# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow manager endpoints."""
import logging
import operator
from typing import Any, Dict
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordBearer
from scanhub_libraries.models import (
    ScanJob,
    TaskOut,
    WorkflowOut,
)
from scanhub_libraries.security import get_current_user

from .orchestration_engine import OrchestrationEngine

router = APIRouter(dependencies=[Depends(get_current_user)])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

orchestration_engine = OrchestrationEngine()

SEQUENCE_MANAGER_URI = "host.docker.internal:8003"
EXAM_MANAGER_URI = "host.docker.internal:8004"

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


@router.get("/hello/")
async def hello_world() -> dict[str, str]:
    """Hello world endpoint."""
    return {"message": "Hello, World!"}

@router.post("/trigger_task/{task_id}/")
async def trigger_task(task_id: str) -> dict[str, Any]:
    """
    Endpoint to trigger a task in the orchestration engine.

    Args:
        task_id (str): The ID of the DAG to be triggered.

    Returns
    -------
        dict: A dictionary containing the response from the orchestration engine.
    """
    print(f"Triggering task: {task_id}")
    try:
        response = orchestration_engine.trigger_task(task_id)
        return {"status": "success", "data": response}
    except Exception as e:
        logging.error(f"Failed to trigger task: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return {"status": "success", "data": "Task triggered successfully"}

@router.get("/tasks/")
async def list_available_tasks():
    """
    Endpoint to list the available tasks from the orchestration engine.
    Currently, only Airflow is supported.

    Returns
    -------
        dict: A dictionary containing the list of available tasks (DAGs) for Airflow.
    """
    try:
        tasks = orchestration_engine.get_available_tasks()
        return {"tasks": tasks}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/process/{workflow_id}/")
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
    """Handle a device task by creating a scan job and starting the scan."""
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
    # await start_scan(job, str(task.id))

    # Update task status to IN_PROGRESS
    task.status = "IN_PROGRESS" # TBD do this also in the data base

    return

async def handle_processing_task(task: TaskOut):
    """Handle a processing task by triggering the appropriate orchestration engine."""
    print("Processing task:")
    print(task.destinations.get("topic"), end="\n")

    # Trigger the orchestration engine to handle the processing task
    orchestration_engine.trigger_task(str(task.id))

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
    # Simulate file upload handling
    file_location = f"/app/data_lake/results/{workflow_id}/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return {"message": "File uploaded successfully"}
