"""Helper functions for dicom."""
import os
from pathlib import Path

from fastapi import HTTPException
from pydicom import dcmread
from pydicom.dataset import FileMetaDataset
from pydicom.filebase import DicomBytesIO
from pydicom.uid import (
    ExplicitVRBigEndian,
    ExplicitVRLittleEndian,
    ImplicitVRLittleEndian,
)

DATA_LAKE_DIR =  Path(os.getenv("DATA_LAKE_DIRECTORY", "/data")).resolve()


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


def is_part10_file(path: Path) -> bool:
    """Return true if file has the DICOM Part-10 preamble (128 zero bytes) and 'DICM' marker at offset 128."""
    with path.open("rb") as f:
        head = f.read(132)
    return len(head) >= 132 and head[128:132] == b"DICM"


def to_part10_bytes(path: str | Path) -> bytes:
    """
    Ensure the dataset at `path` is a valid DICOM Part-10 file.

    - If already Part-10, return its raw bytes unchanged (zero copy via read).
    - If not Part-10, create minimal File Meta + 128-byte preamble and serialize to bytes.
    - We *do not* transcode pixel data here; we only wrap the dataset into Part-10.
    - TransferSyntaxUID:
        * If present, we keep it.
        * If missing, we choose based on ds.is_little_endian/is_implicit_VR if known,
          otherwise default to ExplicitVRLittleEndian (widely supported).
    """
    p = Path(path)

    # Fast path: already Part-10 → return original bytes
    if is_part10_file(p):
        return p.read_bytes()

    # Read whatever is there; force=True accepts raw datasets
    ds = dcmread(str(p), force=True)

    # Ensure File Meta container exists
    if not getattr(ds, "file_meta", None):
        ds.file_meta = FileMetaDataset()

    # Populate mandatory file meta fields when possible
    if not getattr(ds.file_meta, "MediaStorageSOPClassUID", None) and hasattr(ds, "SOPClassUID"):
        ds.file_meta.MediaStorageSOPClassUID = ds.SOPClassUID
    if not getattr(ds.file_meta, "MediaStorageSOPInstanceUID", None) and hasattr(ds, "SOPInstanceUID"):
        ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID

    # Pick/keep a Transfer Syntax
    ts = getattr(ds.file_meta, "TransferSyntaxUID", None)
    if not ts:
        # If dataset's byte order/VR flags are known, mirror them; else default to Explicit VR LE.
        if hasattr(ds, "is_little_endian") and hasattr(ds, "is_implicit_VR"):
            if ds.is_little_endian and ds.is_implicit_VR:
                ts = ImplicitVRLittleEndian
            elif ds.is_little_endian and not ds.is_implicit_VR:
                ts = ExplicitVRLittleEndian
            else:
                ts = ExplicitVRBigEndian
        else:
            ts = ExplicitVRLittleEndian
        ds.file_meta.TransferSyntaxUID = ts

    # Add the 128-byte preamble to make it Part-10
    ds.preamble = b"\x00" * 128

    # Serialize a clean Part-10 file into memory
    bio = DicomBytesIO()
    ds.save_as(bio, write_like_original=False)
    return bio.getvalue()
