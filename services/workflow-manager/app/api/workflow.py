# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow manager endpoints."""

import json
import os

from fastapi import APIRouter, File, HTTPException, UploadFile
from kafka import KafkaProducer # type: ignore
from scanhub import RecoJob # type: ignore

from . import dal
from .models import BaseWorkflow, WorkflowOut, get_workflow_out

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found

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
        List of workflow pydantic output models, might be empty
    """
    if not (workflows := await dal.get_all_workflows()):
        # raise HTTPException(status_code=404, detail="Workflows not found")
        return []
    return [await get_workflow_out(workflow) for workflow in workflows]


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
async def upload_result(record_id: str, file: UploadFile = File(...)) -> dict[str, str]:
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
        reco_id="cartesian", device_id="TB removed", record_id=record_id, input=filename
    )

    # TBD: On successful upload message kafka the correct topic to do reco

    producer.send("mri_cartesian_reco", reco_job)

    # TBD: On successful upload message kafka topic to do reco
    return {"message": f"Successfully uploaded {file.filename}"}


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

# @workflow.get('/download/{record_id}/')
# async def download(record_id: str):
#     file_name = f'cartesian.dcm'
#     file_path = f'/app/data_lake/records/{record_id}/{file_name}'

#     return FileResponse(path=file_path, media_type='application/octet-stream', filename=file_name)
