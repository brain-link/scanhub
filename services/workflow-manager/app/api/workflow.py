# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow manager endpoints."""

import json
import logging
import operator
import os
from typing import Generator, Annotated
from uuid import UUID

import httpx
from fastapi import APIRouter, File, HTTPException, UploadFile, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.security import OAuth2PasswordBearer

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
from scanhub_libraries.security import get_current_user

from .producer import Producer


SEQUENCE_MANAGER_URI = "host.docker.internal:8003"
EXAM_MANAGER_URI = "exam-manager:8000"


router = APIRouter(dependencies=[Depends(get_current_user)])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# Get the producer singleton instance
producer = Producer()



@router.get("/task/process/{task_id}/", tags=["WorkflowManager"])
async def process_task(task_id: UUID | str, access_token: Annotated[str, Depends(oauth2_scheme)]):
    """Process a task.

    Parameters
    ----------
    task_id
        UUID of the task to process

    Returns
    -------
        Task process response
    """

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{EXAM_MANAGER_URI}/api/v1/exam/task/{task_id}", headers={"Authorization": "Bearer " + access_token})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch task with id=" + str(task_id))
        task_raw = response.json()
        task = TaskOut(**task_raw)

        print("Task:")
        print("    id:              ", task.id)
        print("    creator:         ", task.creator)
        print("    datetime_created:", task.datetime_created)
        print("    workflow_id:     ", task.workflow_id)
        print("    name:            ", task.name)
        print("    description:     ", task.description)
        print("    type:            ", task.type)
        print("    args:")
        for key in task.args:
            print("        " + key + ": " + task.args[key])
        print("    artifacts:")
        for key in task.artifacts:
            print("        " + key + ": " + task.artifacts[key])
        print("    destinations:")
        for key in task.destinations:
            print("        " + key + ": " + task.destinations[key])
        print("    status:")
        for key in task.status:
            print("        " + key + ": " + task.status[key])
        print("    is_template:     ", task.is_template)
        print("    is_frozen:       ", task.is_frozen)

        print("DEBUG return!")
        return

    #     if task.type == "DEVICE_TASK" and "PENDING" in task.status:
    #         print("Device task:")
    #         print(task.destinations.get("device"), end="\n")

    #         # Create a device scan job
    #         job = ScanJob(  job_id=task.id,
    #                         sequence_id=task.args["sequence_id"],
    #                         workflow_id=task.args["workflow_id"],
    #                         device_id=task.destinations["device"],
    #                         acquisition_limits=task.args["acquisition_limits"],
    #                         sequence_parameters=task.args["sequence_parameters"])

    #         # Start scan
    #         await start_scan(job, task.id.toString())

    #         # TBD set task status to "IN_PROGRESS"

    #     if task.type == "PROCESSING_TASK" and task.status == "PENDING":
    #         # print(task.destinations, end="\n")
    #         print("Processing task:")

    #         topic = task.destinations.get("topic")

    #         task_event = TaskEvent(task_id=str(task.id), input=task.args)

    #         print("Task event", end="\n")
    #         print(task_event, end="\n")

    #         print("Send to topic", end="\n")
    #         print(topic, end="\n")

    #         # Send message to Kafka
    #         # await producer.send("mri_cartesian_reco", reco_job.dict())
    #         await producer.send(topic, task_event.dict())

    #         # TBD set task status to "IN_PROGRESS"
    # return




@router.get("/process/{workflow_id}/", tags=["WorkflowManager"])
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

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{EXAM_MANAGER_URI}/api/v1/exam/workflow/{workflow_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch workflow data")
        workflow_raw = response.json()
        workflow = WorkflowOut(**workflow_raw)

        workflow.tasks.sort(key=operator.attrgetter('datetime_created'))
        print("Workflow tasks: ")
        task: TaskOut
        for task in workflow.tasks:
            if task.type == "DEVICE_TASK" and "PENDING" in task.status:
                print("Device task:")
                print(task.destinations.get("device"), end="\n")

                # Create a device scan job
                job = ScanJob(  job_id=task.id,
                                sequence_id=task.args["sequence_id"],
                                workflow_id=task.args["workflow_id"],
                                device_id=task.destinations["device"],
                                acquisition_limits=task.args["acquisition_limits"],
                                sequence_parameters=task.args["sequence_parameters"])

                # Start scan
                await start_scan(job, task.id.toString())

                # TBD set task status to "IN_PROGRESS"

                break

            if task.type == "PROCESSING_TASK" and task.status == "PENDING":
                # print(task.destinations, end="\n")
                print("Processing task:")

                topic = task.destinations.get("topic")

                task_event = TaskEvent(task_id=str(task.id), input=task.args)

                print("Task event", end="\n")
                print(task_event, end="\n")

                print("Send to topic", end="\n")
                print(topic, end="\n")

                # Send message to Kafka
                # await producer.send("mri_cartesian_reco", reco_job.dict())
                await producer.send(topic, task_event.dict())

                # TBD set task status to "IN_PROGRESS"

                break

    return


@router.post("/upload/{workflow_id}/", tags=["WorkflowManager"])
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


@router.get("/download/{record_id}/", tags=["WorkflowManager"])
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


@router.get("/image/{record_id}/", tags=["WorkflowManager"])
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


@router.post("/start-scan", tags=["WorkflowManager"])
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


@router.post("/forward-status", tags=["WorkflowManager"])
async def forward_status(scan_status: ScanStatus):
    """Receives status for a job. Forwards it to the ui and returns ok."""
    print("Received status: %s", scan_status)
    return {"message": "Status submitted"}
