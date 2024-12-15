# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow manager endpoints."""
import asyncio
import httpx
import json
import os
import logging
import operator
from uuid import UUID
from typing import Generator, Dict, Any
from fastapi import HTTPException, UploadFile, File, APIRouter, status
from fastapi.responses import FileResponse, StreamingResponse

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
from aiokafka import AIOKafkaConsumer

router = APIRouter()

SEQUENCE_MANAGER_URI = "host.docker.internal:8003"
EXAM_MANAGER_URI = "host.docker.internal:8004"

producer = Producer()

# In-memory workflow storage
# {
#   "workflow_id": {
#     "tasks": [
#         {"id": <task_id>, "type": <task_type>, "status": "PENDING|IN_PROGRESS|COMPLETED|FAILED", 
#          "destinations": {...}, "args": {...}}
#     ],
#     "status": "running|completed|failed"
#   }
# }
workflows: Dict[str, Dict[str, Any]] = {}

# Kafka Topics
WORKFLOW_REQUESTS_TOPIC = "workflow-requests"
TASK_ASSIGNMENTS_TOPIC = "task-assignments"
TASK_COMPLETIONS_TOPIC = "task-completions"
WORKFLOW_RESPONSES_TOPIC = "workflow-responses"

# Consumer for workflow requests (start_workflow, get_status)
async def consume_workflow_requests():
    consumer = AIOKafkaConsumer(
        WORKFLOW_REQUESTS_TOPIC,
        bootstrap_servers='localhost:9092',
        group_id="workflow_manager_requests"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            message = json.loads(msg.value)
            req_type = message.get("type")
            workflow_id = message.get("workflow_id")

            if req_type == "start_workflow":
                await start_workflow(workflow_id)
            elif req_type == "get_status":
                await send_workflow_status(workflow_id)
    finally:
        await consumer.stop()

# Consumer for task completions
async def consume_task_completions():
    consumer = AIOKafkaConsumer(
        TASK_COMPLETIONS_TOPIC,
        bootstrap_servers='localhost:9092',
        group_id="workflow_manager_completions"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            message = json.loads(msg.value)
            workflow_id = message['workflow_id']
            task_id = message['task_id']
            success = message.get('success', True)
            await handle_finished_task(workflow_id, task_id, success)
    finally:
        await consumer.stop()

async def start_workflow(workflow_id: str):
    """Fetch and initialize a workflow, then dispatch the first task."""
    # Fetch workflow data
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{EXAM_MANAGER_URI}/api/v1/exam/workflow/{workflow_id}")
        if response.status_code != 200:
            logging.error("Failed to fetch workflow data")
            return
        workflow_raw = response.json()
        workflow = WorkflowOut(**workflow_raw)

        # Sort tasks by datetime_created
        workflow.tasks.sort(key=operator.attrgetter('datetime_created'))

        # Initialize workflow in-memory
        workflows[workflow_id] = {
            "tasks": [ 
                {
                    "id": t.id,
                    "type": t.type,
                    "status": t.status,
                    "destinations": t.destinations,
                    "args": t.args
                } for t in workflow.tasks
            ],
            "status": "running"
        }

    # Dispatch the first pending task if any
    await dispatch_next_task(workflow_id)

    # Send status response
    await send_workflow_status(workflow_id)

async def dispatch_next_task(workflow_id: str):
    """Find the next pending task and dispatch it."""
    wf = workflows.get(workflow_id)
    if not wf:
        return

    for t in wf["tasks"]:
        if t["status"] == "PENDING":
            # Dispatch task
            if t["type"] == "DEVICE_TASK":
                await handle_device_task(workflow_id, t)
            elif t["type"] == "PROCESSING_TASK":
                await handle_processing_task(workflow_id, t)
            return

    # If no pending tasks, workflow may be completed
    all_completed = all(task["status"] in ("COMPLETED", "FAILED") for task in wf["tasks"])
    if all_completed:
        wf["status"] = "completed"
        await send_workflow_status(workflow_id)

async def handle_finished_task(workflow_id: str, task_id: str, success: bool):
    """Update task status and dispatch next task if successful."""
    wf = workflows.get(workflow_id)
    if not wf:
        logging.error(f"Unknown workflow_id {workflow_id}")
        return

    # Update task status
    for t in wf["tasks"]:
        if str(t["id"]) == str(task_id):
            t["status"] = "COMPLETED" if success else "FAILED"
            break

    if success:
        # Dispatch next task if available
        await dispatch_next_task(workflow_id)
    else:
        wf["status"] = "failed"
        await send_workflow_status(workflow_id)

async def send_workflow_status(workflow_id: str):
    """Produce a message with the current workflow status to workflow-responses."""
    wf = workflows.get(workflow_id)
    if not wf:
        # Unknown workflow
        msg = {"workflow_id": workflow_id, "status": "unknown", "tasks": []}
    else:
        msg = {
            "workflow_id": workflow_id,
            "status": wf["status"],
            "tasks": wf["tasks"]
        }
    await producer.send(WORKFLOW_RESPONSES_TOPIC, msg)

async def handle_device_task(workflow_id: str, task: dict):
    """Handle a device task by starting the scan."""
    # Mark as in-progress
    task["status"] = "IN_PROGRESS"
    job = ScanJob(
        job_id=task["id"],
        sequence_id=task["args"]["sequence_id"],
        workflow_id=task["args"]["workflow_id"],
        device_id=task["destinations"]["device"],
        acquisition_limits=task["args"]["acquisition_limits"],
        sequence_parameters=task["args"]["sequence_parameters"]
    )
    await start_scan(job, str(task["id"]))

async def handle_processing_task(workflow_id: str, task: dict):
    """Handle a processing task by sending it to the specified topic."""
    task["status"] = "IN_PROGRESS"
    topic = task["destinations"].get("topic")
    task_event = TaskEvent(task_id=str(task["id"]), input=task["args"])
    # Send the task event to the assignment topic
    await producer.send(TASK_ASSIGNMENTS_TOPIC, {
        "workflow_id": workflow_id,
        "task_id": str(task["id"]),
        "input": task_event.dict()
    })

@router.get("/process/{workflow_id}/")
async def process(workflow_id: UUID | str) -> dict[str, str]:
    """Process a workflow - start or continue workflow if needed."""
    workflow_id = str(workflow_id)
    # If workflow not started yet, start it
    if workflow_id not in workflows:
        await start_workflow(workflow_id)
    else:
        # If already known, just attempt to dispatch next task
        await dispatch_next_task(workflow_id)
    return {"message": "Workflow processed successfully"}

@router.post("/upload/{workflow_id}/")
async def upload_result(workflow_id: str, file: UploadFile = File(...)) -> dict[str, str]:
    """Upload workflow result, then try to dispatch next tasks."""
    filename = f"records/{workflow_id}/{file.filename}"
    try:
        contents = file.file.read()
        app_filename = f"/app/data_lake/{filename}"
        os.makedirs(os.path.dirname(app_filename), exist_ok=True)
        with open(app_filename, "wb") as filehandle:
            filehandle.write(contents)
    except Exception as ex:
        return {"message": "Error uploading file: " + str(ex)}
    finally:
        file.file.close()

    # After uploading, attempt to continue the workflow
    await dispatch_next_task(workflow_id)

    return {"message": f"Successfully uploaded {file.filename}"}

@router.get("/download/{record_id}/")
async def download_result(record_id: int) -> FileResponse:
    file_name = f"record-{record_id}.dcm"
    file_path = f"/app/data_lake/records/{record_id}/{file_name}"
    return FileResponse(path=file_path, media_type="application/octet-stream", filename=file_name)

def get_data_from_file(file_path: str) -> Generator:
    with open(file=file_path, mode="rb") as file_like:
        yield file_like.read()

@router.get("/image/{record_id}/")
async def get_image_file(record_id: int) -> StreamingResponse:
    file_name = f"record-{record_id}.dcm"
    file_path = f"/app/data_lake/records/{record_id}/{file_name}"
    try:
        file_contents = get_data_from_file(file_path=file_path)
        response = StreamingResponse(
            content=file_contents,
            status_code=status.HTTP_200_OK,
            media_type="application/octet-stream",
        )
        return response
    except FileNotFoundError as exc:
        raise HTTPException(detail="File not found.", status_code=status.HTTP_404_NOT_FOUND) from exc

async def device_location_request(device_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://api-gateway:8080/api/v1/device/{device_id}/ip_address")
        return response.json()["ip_address"]

async def retrieve_sequence(sequence_manager_uri, sequence_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{sequence_manager_uri}/api/v1/mri/sequences/{sequence_id}")
        return response.json()

async def post_device_task(url, device_task):
    from fastapi.encoders import jsonable_encoder
    async with httpx.AsyncClient() as client:
        data = json.dumps(device_task, default=jsonable_encoder)
        response = await client.post(url, content=data)
        return response.status_code

@router.post("/start-scan")
async def start_scan(scan_job: ScanJob, task_id: str):
    device_id = scan_job.device_id
    command = Commands.START

    device_ip = await device_location_request(device_id)
    url = f"http://{device_ip}/api/start-scan"
    sequence_json = await retrieve_sequence(SEQUENCE_MANAGER_URI, scan_job.sequence_id)

    record_id = task_id
    parametrized_sequence = ParametrizedSequence(
        acquisition_limits=scan_job.acquisition_limits,
        sequence_parameters=scan_job.sequence_parameters,
        sequence=json.dumps(sequence_json),
    )

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
    print("Received status:", scan_status)
    return {"message": "Status submitted"}

# Start the Kafka consumers in the background
loop = asyncio.get_event_loop()
loop.create_task(consume_workflow_requests())
loop.create_task(consume_task_completions())
