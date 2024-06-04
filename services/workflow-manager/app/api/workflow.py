# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow manager endpoints."""

import os
from typing import Generator

import httpx
import pydantic
import dataclasses
import json


from uuid import UUID

from datetime import datetime

import operator
import json

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, StreamingResponse
from scanhub_libraries.models import TaskOut, WorkflowOut

# from scanhub import RecoJob # type: ignore
from pydantic import BaseModel, StrictStr

from .producer import Producer

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found


EXAM_MANAGER_URI = "host.docker.internal:8004"


class TaskEvent(BaseModel):
    """Task Event"""  # noqa: E501

    task_id: str
    input: dict[str, str] 

router = APIRouter()

# Get the producer singleton instance
producer = Producer()


@router.get("/process/{workflow_id}/")
async def process(workflow_id: UUID | str):
    """Process a workflow.

    Parameters
    ----------
    workflow_id
        UUID of the workflow to process

    Returns
    -------
        Workflow process response
    """

    # Debugging
    workflow_id = 'ae7d4105-8312-436f-bc48-98f57c2fe86d' #'cec25959-c451-4faf-9093-97431aba41e6'
    
    exam_manager_uri = EXAM_MANAGER_URI


    async with httpx.AsyncClient() as client:
        # TODO: data_path, comment ? # pylint: disable=fixme
        response = await client.get(f"http://{exam_manager_uri}/api/v1/exam/workflow/{workflow_id}")

        assert response.status_code == 200  # noqa: S101

        workflow_raw = response.json()
        workflow = WorkflowOut(**workflow_raw)
        
        print("Workflow tasks: ")

        # Sort the tasks by datetime_created
        workflow.tasks.sort(key=operator.attrgetter('datetime_created'))

        task: TaskOut
        for task in workflow.tasks:
            # Debugging
            # print(task.id, end="\n")
            # print(task.type, end="\n")
            # print(task.description if task.description else "No description", end="\n")

            if task.type == "DEVICE_TASK":
                print("Device task:") 
                print(task.destinations.get("device"), end="\n")
                # reco_job = RecoJob(record_id=task.id, input=task.args["input"])
                # # Send message to Kafka
                # await producer.send("mri_cartesian_reco", reco_job.dict())

            if task.type == "PROCESSING_TASK":
                # print(task.destinations, end="\n")
                print("Processing task:")

                topic = task.destinations.get("topic")

                task_event = TaskEvent(task_id=str(task.id), input=task.args)

                print("Task event", end="\n")
                print(task_event, end="\n")

                print("Send to topic", end="\n")
                print(topic, end="\n")

                # # Send message to Kafka
                # await producer.send("mri_cartesian_reco", reco_job.dict())
                await producer.send(topic, task_event.dict())



            # workflow_id: Optional[UUID] = None  # Field("", description="ID of the workflow the task belongs to.")
            # description: str
            # type: TaskType
            # args: dict[str, str]
            # artifacts: dict[str, str]
            # destinations: dict[str, str]
            # # artifacts: dict[str, list[dict[str, str]]]
            # # task_destinations: list[dict[str, str]]
            # status: dict[TaskStatus, str]
            # is_template: bool
            # is_frozen: bool


            # id: UUID
            # datetime_created: datetime

          

            # Send message to Kafka
            # await producer.send("mri_cartesian_reco", RecoJob(record_id=task.task_id, input=task.task_input).dict())

    return







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
