# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow manager endpoints."""

import os
from typing import Generator

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, StreamingResponse

# from scanhub import RecoJob # type: ignore
from pydantic import BaseModel, StrictStr

from .producer import Producer

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found


class RecoJob(BaseModel):
    """RecoJob is a pydantic model for a reco job."""  # noqa: E501

    record_id: int
    input: StrictStr


router = APIRouter()

# Get the producer singleton instance
producer = Producer()


@router.post("/upload/{record_id}/")
async def upload_result(record_id: int, file: UploadFile = File(...)) -> dict[str, str]:
    """Upload workflow result.

    Parameters
    ----------
    record_id
        Id of the record, which is processed by workflow
    file, optional
        Data upload, e.g. reconstruction result, by default File(...)

    Returns
    -------
        Notification
    """
    filename = f"records/{record_id}/{file.filename}"

    try:
        contents = file.file.read()
        app_filename = f"/app/data_lake/{filename}"
        os.makedirs(os.path.dirname(app_filename), exist_ok=True)
        with open(app_filename, "wb") as filehandle:
            filehandle.write(contents)
    except Exception as ex:  # pylint: disable=broad-except
        return {"message": "There was an error uploading the file" + str(ex)}
        # raise HTTPException(status_code = 500, detail = "")
    finally:
        file.file.close()

    # TBD: switch based on the preselected reco

    reco_job = RecoJob(record_id=record_id, input=filename)

    # TBD: On successful upload message kafka the correct topic to do reco

    # Send message to Kafka
    await producer.send("mri_cartesian_reco", reco_job.dict())

    # TBD: On successful upload message kafka topic to do reco
    return {"message": f"Successfully uploaded {file.filename}"}


@router.get("/download/{record_id}/")
async def download_result(record_id: int) -> FileResponse:
    """Download DICOM result.

    Parameters
    ----------
    record_id
        ID of the record the DICOM file belongs to.

    Returns
    -------
        DICOM file response
    """
    file_name = f"record-{record_id}.dcm"
    file_path = f"/app/data_lake/records/{record_id}/{file_name}"

    return FileResponse(path=file_path, media_type="application/octet-stream", filename=file_name)


def get_data_from_file(file_path: str) -> Generator:
    """Open a file and read the data.

    Parameters
    ----------
    file_path
        Path of the file to open

    Yields
    ------
        File content
    """
    with open(file=file_path, mode="rb") as file_like:
        yield file_like.read()


@router.get("/image/{record_id}/")
async def get_image_file(record_id: int) -> StreamingResponse:
    """Read image file data and content as streaming response.

    Parameters
    ----------
    record_id
        Record ID the image should be read for

    Returns
    -------
        Image file content

    Raises
    ------
    HTTPException
        File not found
    """
    file_name = f"record-{record_id}.dcm"
    file_path = f"/app/data_lake/records/{record_id}/{file_name}"
    try:
        file_contents = get_data_from_file(file_path=file_path)
        response = StreamingResponse(
            content=file_contents,
            status_code=status.HTTP_200_OK,
            media_type="text/html",
        )
        return response
    except FileNotFoundError as exc:
        raise HTTPException(detail="File not found.", status_code=status.HTTP_404_NOT_FOUND) from exc
