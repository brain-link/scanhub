# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow manager endpoints."""

import os
from typing import Generator

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, StreamingResponse

# from scanhub import RecoJob # type: ignore
from pydantic import BaseModel, StrictStr

from . import dal
from .models import BaseWorkflow, WorkflowIn, WorkflowMetaOut, WorkflowOut, get_workflow_meta_out, get_workflow_out
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


@router.post("/", response_model=WorkflowOut, status_code=201, tags=["workflow"])
async def create_workflow(payload: WorkflowIn) -> WorkflowOut:
    """Create new workflow endpoint.

    Parameters
    ----------
    payload
        Data to be added, workflow iutput model

    Returns
    -------
        Workflow pydantic output model

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    if not (workflow := await dal.add_workflow(payload)):
        raise HTTPException(status_code=404, detail="Could not create workflow")
    return await get_workflow_out(workflow)


@router.get("/{workflow_id}", response_model=WorkflowOut, status_code=200, tags=["workflow"])
async def get_workflow(workflow_id: int) -> WorkflowOut:
    """Get workflow endpoint.

    Parameters
    ----------
    workflow_id
        Id of the workflow object to be returned

    Returns
    -------
        Workflow pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    if not (workflow := await dal.get_workflow(workflow_id)):
        raise HTTPException(status_code=404, detail="Workflow not found")
    return await get_workflow_out(workflow)


@router.get("/", response_model=list[WorkflowOut], status_code=200, tags=["workflow"])
async def get_workflow_list() -> list[WorkflowOut]:
    """Get all workflows endpoint.

    Returns
    -------
        List of workflow meta pydantic output models, might be empty
    """
    if not (workflows := await dal.get_all_workflows()):
        # raise HTTPException(status_code=404, detail="Workflows not found")
        return []
    return [await get_workflow_out(workflow) for workflow in workflows]


@router.get("/meta/", response_model=list[WorkflowMetaOut], status_code=200, tags=["workflow"])
async def get_workflow_meta_list() -> list[WorkflowMetaOut]:
    """Get all workflow meta information endpoint.

    Returns
    -------
        List of workflow meta pydantic output models, might be empty
    """
    if not (workflows := await dal.get_all_workflows()):
        # raise HTTPException(status_code=404, detail="Workflows not found")
        return []
    return [await get_workflow_meta_out(workflow) for workflow in workflows]


@router.delete("/{workflow_id}", response_model={}, status_code=204, tags=["workflow"])
async def delete_workflow(workflow_id: int) -> None:
    """Delete workflow endpoint.

    Parameters
    ----------
    workflow_id
        Id of workflow to be deleted

    Raises
    ------
    HTTPException
        404: Not found
    """
    if not await dal.delete_workflow(workflow_id):
        raise HTTPException(status_code=404, detail="Workflow not found")


@router.put("/{workflow_id}/", response_model=WorkflowOut, status_code=200, tags=["workflow"])
async def update_workflow(workflow_id: int, payload: BaseWorkflow) -> WorkflowOut:
    """Update existing workflow endpoint.

    Parameters
    ----------
    workflow_id
        Id of the workflow to be updated
    payload
        Data to be updated, workflow pydantic base model

    Returns
    -------
        Workflow pydantic output model.

    Raises
    ------
    HTTPException
        404: Not found
    """
    if not (workflow := await dal.update_workflow(workflow_id, payload)):
        raise HTTPException(status_code=404, detail="Workflow not found")
    return await get_workflow_out(workflow)


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


    # retrieve number of workflows from db
    # print("Number of workflows in db: ", await dal.count_workflows())
    
    # if dal.get_workflow(record_id) is None:

    # workflow_id = 1

    # workflow = await dal.get_workflow(workflow_id)


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
