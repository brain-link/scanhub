"""Helper functions for dicom."""

import io
import os
from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydicom import dcmread
from pydicom.dataset import FileMetaDataset
from pydicom.filebase import DicomBytesIO
from pydicom.uid import (
    ExplicitVRBigEndian,
    ExplicitVRLittleEndian,
    ImplicitVRLittleEndian,
)
from starlette.responses import Response

DATA_LAKE_DIR = Path(os.getenv("DATA_LAKE_DIRECTORY", "/data")).resolve()


def resolve_dicom_path(workflow_id: str, task_id: str, result_id: str, filename: str) -> Path:
    """Build and validate the requested file path, prevent traversal, return (path, safe_name)."""
    safe_name = Path(filename).name  # strip any path components
    requested = (DATA_LAKE_DIR / workflow_id / task_id / result_id / safe_name).resolve()

    # Ensure request stays under BASE
    try:
        if not requested.is_relative_to(DATA_LAKE_DIR):
            raise ValueError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file path")

    if not requested.exists():
        raise HTTPException(status_code=404, detail=f"Dicom file does not exist: {requested}")

    return requested


def provide_p10_dicom(dicom_path: str | Path) -> Response:
    """
    Ensure the dataset at `path` is a valid DICOM Part-10 file.

    - If already Part-10, return FileResponse
    - If not Part-10, create minimal File Meta + 128-byte preamble and return StreamingResponse
    - We *do not* transcode pixel data here; we only wrap the dataset into Part-10.
    - TransferSyntaxUID:
        * If present, we keep it.
        * If missing, we choose based on ds.is_little_endian/is_implicit_VR if known,
          otherwise default to ExplicitVRLittleEndian (widely supported).
    """
    path = Path(dicom_path)

    # If already Part-10, return raw bytes
    with path.open("rb") as f:
        head = f.read(132)
    # Check if header is P10
    if len(head) >= 132 and head[128:132] == b"DICM":
        # FastAPI's FileResponse automatically handles Range requests
        return FileResponse(
            path=path,
            media_type="application/dicom",
            filename=path.name,
            headers={
                "X-Content-Type-Options": "nosniff",
                "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0, no-transform",
            },
        )

    # Read whatever is there; force=True accepts raw datasets
    ds = dcmread(str(path), force=True)

    if not getattr(ds, "file_meta", None):
        ds.file_meta = FileMetaDataset()
    if not getattr(ds.file_meta, "MediaStorageSOPClassUID", None) and hasattr(ds, "SOPClassUID"):
        ds.file_meta.MediaStorageSOPClassUID = ds.SOPClassUID
    if not getattr(ds.file_meta, "MediaStorageSOPInstanceUID", None) and hasattr(ds, "SOPInstanceUID"):
        ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID

    if not getattr(ds.file_meta, "TransferSyntaxUID", None):
        if hasattr(ds, "is_little_endian") and hasattr(ds, "is_implicit_VR"):
            ds.file_meta.TransferSyntaxUID = (
                ImplicitVRLittleEndian
                if ds.is_little_endian and ds.is_implicit_VR
                else ExplicitVRLittleEndian
                if ds.is_little_endian
                else ExplicitVRBigEndian
            )
        else:
            ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    # Add the 128-byte preamble to make it Part-10
    ds.preamble = b"\x00" * 128

    # Serialize a clean Part-10 file into memory
    bio = DicomBytesIO()
    ds.save_as(bio, write_like_original=False)
    data = bio.getvalue()

    if len(data) < 132 or data[128:132] != b"DICM":
        raise HTTPException(status_code=500, detail="Internal error: produced bytes are not valid DICOM Part-10 format")

    return StreamingResponse(
        io.BytesIO(data),
        media_type="application/dicom",
        headers={
            "Content-Disposition": f'inline; filename="{path.name}"',
            "X-Content-Type-Options": "nosniff",
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0, no-transform",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )
