# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow manager endpoints."""

import asyncio
import httpx
import json
import os
import logging
from uuid import UUID
from typing import Generator
from fastapi import HTTPException, UploadFile, File, APIRouter
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
# from some_module import EXAM_MANAGER_URI, SEQUENCE_MANAGER_URI, TaskOut, WorkflowOut, ScanJob, TaskEvent, DeviceTask, ParametrizedSequence, Commands, ScanStatus
from aiokafka import AIOKafkaConsumer

from dal import update_task_status, get_workflow_id_by_task_id


# from scanhub import RecoJob # type: ignore
from scanhub_libraries.models import (
    Commands,
    DeviceTask,
    ParametrizedSequence,
    ScanJob,
    ScanStatus,
    TaskEvent,
    TaskOut,
    WorkflowOut,
)

from .producer import Producer

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found


SEQUENCE_MANAGER_URI = "host.docker.internal:8003"
EXAM_MANAGER_URI = "host.docker.internal:8004"


router = APIRouter()

# Get the producer singleton instance
producer = Producer()

# Kafka consumer setup
async def consume_finished_tasks():
    """Consume finished tasks from the Kafka topic and handle them."""
    consumer = AIOKafkaConsumer(
        'task_completion_events',
        bootstrap_servers='localhost:9092',
        group_id="workflow_manager"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            message = json.loads(msg.value)
            task_id = message['task_id']
            status = message['status']
            await handle_finished_task(task_id, status)
    finally:
        await consumer.stop()


async def handle_finished_task(task_id: str, status: str):
    """Handle finished task by updating the task status and processing the next task.
    
    Parameters
    ----------
    task_id
        ID of the task to handle
    status
        Status of the task
    """
    # Update task status in the database
    await update_task_status_in_db(task_id, status)

    # Fetch the workflow ID associated with the task
    workflow_id = await get_workflow_id_by_task_id(task_id)

    # Process the next pending task
    await process(workflow_id)


async def update_task_status_in_db(task_id: str, status: str):
    """Update the task status in the database.
    
    Parameters
    ----------
    task_id
        ID of the task to update
    status
        New status of the task
    """
    # Simulate updating the database
    print(f"Updating task {task_id} status to {status} in the database")

async def get_workflow_id_by_task_id(task_id: str) -> str:
    """Fetch the workflow ID associated with the task ID."""
    # Simulate fetching the workflow ID from the database
    return "some-workflow-id"


@router.get("/process/{workflow_id}/")
async def process(workflow_id: UUID | str) -> dict[str, str]:
    """Process a workflow.

    Parameters
    ----------
    workflow_id
        UUID of the workflow to process

    Returns
    -------
        Workflow process response
    """
    # Debugging: Remove hardcoded workflow_id and use the provided one
    workflow_id = 'ae7d4105-8312-436f-bc48-98f57c2fe86d' #'cec25959-c451-4faf-9093-97431aba41e6'

    # URI for the exam manager service
    exam_manager_uri = EXAM_MANAGER_URI
    # Create an asynchronous HTTP client
    async with httpx.AsyncClient() as client:
        # Fetch the workflow data from the exam manager service
        response = await client.get(f"http://{exam_manager_uri}/api/v1/exam/workflow/{workflow_id}")
        # Raise an exception if the request was not successful
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch workflow data")
        # Parse the response JSON into a WorkflowOut object
        workflow_raw = response.json()
        workflow = WorkflowOut(**workflow_raw)
        # Sort the tasks by datetime_created
        workflow.tasks.sort(key=operator.attrgetter('datetime_created'))
        task: TaskOut
        # Iterate through the tasks and handle them based on their type and status
        for task in workflow.tasks:
            if task.type == "DEVICE_TASK" and task.status == "PENDING":
                # Handle device task
                await handle_device_task(task)
                break  # Exit after handling the first pending task
            elif task.type == "PROCESSING_TASK" and task.status == "PENDING":
                # Handle processing task
                await handle_processing_task(task)
                break  # Exit after handling the first pending task
    return {"message": "Workflow processed successfully"}


async def handle_device_task(task: TaskOut):
    """Handle a device task by creating a scan job and starting the scan.
    
    Parameters
    ----------
    task
        Task to handle
    """
    print("Device task:")
    print(task.destinations.get("device"), end="\n")

    # Create a device scan job
    job = ScanJob(
        job_id=task.id,
        sequence_id=task.args["sequence_id"],
        workflow_id=task.args["workflow_id"],
        device_id=task.destinations["device"],
        acquisition_limits=task.args["acquisition_limits"],
        sequence_parameters=task.args["sequence_parameters"]
    )

    # Start the scan job
    await start_scan(job, str(task.id))

    # Update task status to IN_PROGRESS
    task.status = "IN_PROGRESS" # TBD do this also in the data base

    return


async def handle_processing_task(task: TaskOut):
    """Handle a processing task by sending a message to the appropriate Kafka topic.
    
    Parameters
    ----------
    task
        Task to handle
    """
    print("Processing task:")
    topic = task.destinations.get("topic")

    # Create a task event
    task_event = TaskEvent(task_id=str(task.id), input=task.args)

    # Debugging: Print task event and topic
    print("Task event", end="\n")
    print(task_event, end="\n")
    print("Send to topic", end="\n")
    print(topic, end="\n")

    # Send the task event to the Kafka topic
    await producer.send(topic, task_event.dict())

    # Update task status to IN_PROGRESS
    task.status = "IN_PROGRESS" # TBD do this also in the data base

    return


@router.post("/upload/{workflow_id}/")
async def upload_result(workflow_id: str, file: UploadFile = File(...)) -> dict[str, str]:
    """Upload workflow result.

    Parameters
    ----------
    workflow_id
        Id of the workflow, which is processed by workflow
    file, optional
        Data upload, e.g. reconstruction result, by default File(...)

    Returns
    -------
        Notification
    """
    filename = f"records/{workflow_id}/{file.filename}"

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

    # Start Processing Task
    await process(workflow_id)

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

## Formerly acquisition control

async def device_location_request(device_id):
    """Retrieve ip from device-manager.

    Parameters
    ----------
    device_id
        Id of device

    Returns
    -------
        ip_address of device
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://api-gateway:8080/api/v1/device/{device_id}/ip_address")
        return response.json()["ip_address"]


async def retrieve_sequence(sequence_manager_uri, sequence_id):
    """Retrieve sequence and sequence-type from sequence-manager.

    Parameters
    ----------
    sequence_manager_uri
        uri of sequence manager

    sequence_id
        id of sequence

    Returns
    -------
        sequence
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{sequence_manager_uri}/api/v1/mri/sequences/{sequence_id}")
        return response.json()


async def create_record(exam_manager_uri, job_id):
    """Create new record at exam_manager and retrieve record_id.

    Parameters
    ----------
    exam_manager_uri
        uri of sequence manager

    job_id
        id of job

    Returns
    -------
        id of newly created record
    """
    # async with httpx.AsyncClient() as client:
    #     # TODO: data_path, comment ? # pylint: disable=fixme
    #     data = {
    #         "data_path": "unknown",
    #         "comment": "Created in Acquisition Control",
    #         "job_id": str(job_id),
    #     }
    #     response = await client.post(f"http://{exam_manager_uri}/api/v1/exam/record", json=data)
    #     return response.json()["id"]

    print("Error: Create Record not yet implmented:", job_id)


async def post_device_task(url, device_task):
    """Send task do device.

    Parameters
    ----------
    url
        url of the device

    device_task
        task

    Returns
    -------
        response of device
    """
    async with httpx.AsyncClient() as client:
        data = json.dumps(device_task, default=jsonable_encoder)
        response = await client.post(url, content=data)
        return response.status_code


@router.post("/start-scan")
async def start_scan(scan_job: ScanJob, task_id: str):
    """Receives a job. Create a record id, trigger scan with it and returns it."""
    device_id = scan_job.device_id
    record_id = ""
    command = Commands.START

    device_ip = await device_location_request(device_id)
    url = f"http://{device_ip}/api/start-scan"

    print("Start-scan endpoint, device ip: ", device_ip)

    # get sequence
    sequence_json = await retrieve_sequence(SEQUENCE_MANAGER_URI, scan_job.sequence_id)

    # create record
    record_id = task_id#await create_record(EXAM_MANAGER_URI, scan_job.job_id)
    parametrized_sequence = ParametrizedSequence(
        acquisition_limits=scan_job.acquisition_limits,
        sequence_parameters=scan_job.sequence_parameters,
        sequence=json.dumps(sequence_json),
    )

    # start scan and forward sequence, workflow, record_id
    logging.debug("Received job: %s, Generated record id: %s", scan_job.job_id, record_id)

    device_task = DeviceTask(
        device_id=device_id, record_id=record_id, command=command, parametrized_sequence=parametrized_sequence
    )
    status_code = await post_device_task(url, device_task)

    if status_code == 200:
        print("Scan started successfully.")
    else:
        print("Failed to start scan.")
    return {"record_id": record_id}


@router.post("/forward-status")
async def forward_status(scan_status: ScanStatus):
    """Receives status for a job. Forwards it to the ui and returns ok."""
    print("Received status: %s", scan_status)
    return {"message": "Status submitted"}


# Start the Kafka consumer in the background
loop = asyncio.get_event_loop()
loop.create_task(consume_finished_tasks())
