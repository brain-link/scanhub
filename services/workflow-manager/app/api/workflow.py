# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow manager endpoints."""

import json
import os

from typing import Generator

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, StreamingResponse

from kafka import KafkaProducer # type: ignore
# from scanhub import RecoJob # type: ignore
from pydantic import BaseModel, StrictStr


from . import dal
from .models import BaseWorkflow, WorkflowMetaOut, WorkflowOut, get_workflow_meta_out, get_workflow_out

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found

class RecoJob(BaseModel):
    """RecoJob is a pydantic model for a reco job.""" # noqa: E501
    record_id: int
    input: StrictStr



producer = KafkaProducer(
    bootstrap_servers=["kafka-broker:9093"],
    value_serializer=lambda x: json.dumps(x.__dict__).encode("utf-8"),
)

router = APIRouter()


@router.post("/", response_model=WorkflowOut, status_code=201, tags=["workflow"])
async def create_workflow(payload: BaseWorkflow) -> WorkflowOut:
    """Create new workflow endpoint.

    Parameters
    ----------
    payload
        Workflow pydantic base model

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


@router.get(
    "/{workflow_id}", response_model=WorkflowOut, status_code=200, tags=["workflow"]
)
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


@router.put(
    "/{workflow_id}/", response_model=WorkflowOut, status_code=200, tags=["workflow"]
)
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


# ****\\ OLD CODE //****

# @workflow.post('/', response_model=WorkflowOut, status_code=201)
# async def create_workflow(payload: WorkflowIn):
#     workflow_id = await db_manager.add_workflow(payload)

#     response = {
#         'id': workflow_id,
#         **payload.dict()
#     }

#     return response


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

    reco_job = RecoJob(
        record_id=record_id, input=filename
    )

    # TBD: On successful upload message kafka the correct topic to do reco

    producer.send("mri_cartesian_reco", reco_job)



    # TBD: On successful upload message kafka topic to do reco
    return {"message": f"Successfully uploaded {file.filename}"}


@router.get('/download/{record_id}/')
async def download_result(record_id: int):
    file_name = f"record-{record_id}.dcm"
    file_path = f'/app/data_lake/records/{record_id}/{file_name}'

    return FileResponse(path=file_path, media_type='application/octet-stream', filename=file_name)

# #EXAMPLE: http://localhost:8080/api/v1/workflow/control/start/
# TBD: frontend neesds to call a generic endpoint to trigger the acquisition
# #@workflow.post('/control/{device_id}/{record_id}/{command}')
# @workflow.post('/control/{command}/')
# async def acquistion_control(command: str):
#     try:
#         acquisition_command = AcquisitionCommand[command]
#     except KeyError:
#         print('KeyError: acquisition command not found')

#     device_id = 'mri_simulator' #DEBUG: this should be the device_id from the frontend
#     record_id = uuid.uuid4() #DEBUG: this should be the record_id from the frontend
#     input_sequence = 'input_sequence' #DEBUG: this should be the input_sequence from the frontend

#     acquisition_event = AcquisitionEvent(   device_id=device_id,
#                                             record_id=record_id,
#                                             command_id=acquisition_command,
#                                             input_sequence=input_sequence)
#     producer.send('acquisitionEvent', acquisition_event)
#     return {"message": f"Triggered {acquisition_event}"}

# A simple method to open the file and get the data
def get_data_from_file(file_path: str) -> Generator:
    with open(file=file_path, mode="rb") as file_like:
        yield file_like.read()

# Now response the API
@router.get('/image/{record_id}/')
async def get_image_file(record_id: int):
    file_name = f"record-{record_id}.dcm"
    file_path = f'/app/data_lake/records/{record_id}/{file_name}'
    try:
        file_contents = get_data_from_file(file_path=file_path)
        response = StreamingResponse(
            content=file_contents,
            status_code=status.HTTP_200_OK,
            media_type="text/html",
        )
        return response
    except FileNotFoundError:
        raise HTTPException(detail="File not found.", status_code=status.HTTP_404_NOT_FOUND)