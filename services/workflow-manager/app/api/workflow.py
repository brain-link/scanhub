# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""
Workflow manager endpoints.

TODO: How to handle tasks, and where to trigger the device task?
- There should be one endpoint for task, workflow and exam
- The endpoint processes the list, i.e. all the contained tasks
- Does it help to store an index with each task?
- Which endpoint triggers the acquisition? (devicem manager?)
- cleanup: currently there is trigger_task(...) (used by frontend) and process(...)

"""
import json
import logging
import operator
import os
import time
from datetime import date
from typing import Annotated, Any, Dict
from uuid import UUID

import requests
from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from scanhub_libraries.models import (
    AcquisitionLimits,
    AcquisitionTaskOut,
    BaseResult,
    DAGTaskOut,
    ExamOut,
    ItemStatus,
    PatientOut,
    ResultType,
    TaskOut,
    TaskType,
    WorkflowOut,
)
from scanhub_libraries.security import get_current_user

from .orchestration_engine import OrchestrationEngine

router = APIRouter(dependencies=[Depends(get_current_user)])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

orchestration_engine = OrchestrationEngine()

SEQUENCE_MANAGER_URI = "sequence-manager:8000"
EXAM_MANAGER_URI = "exam-manager:8000"
PATIENT_MANAGER_URI = "patient-manager:8100"
DEVICE_MANAGER_URI = "device-manager:8000"


# Read the DATA_LAKE_DIRECTORY environment variable
data_lake_directory = os.getenv('DATA_LAKE_DIRECTORY', '/default/path/if/not/set')

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


@router.get("/hello/", tags=["WorkflowManager"])
async def hello_world() -> dict[str, str]:
    """Hello world endpoint."""
    return {"message": "Hello, World!"}


def simulate_reconstruction_task(task, headers):
    """
    Simulate reconstruction task by updating the task progress and finally creating a result for the task.

    Args:
        task (Task): The task to simulate and that gets updated in the database when (virtual) progress is made.
                     The attribute task.args["contrast"] is expected to be present and will be set as the results filename attribute.
        headers (dict): The headers for calls to the exam-manager.
    """
    print('Simulate reconstruction task.')
    for percentage in [25, 50, 75]:
        time.sleep(2)
        task.progress = percentage
        requests.put(f"http://{EXAM_MANAGER_URI}/api/v1/exam/task/{task.id}",
                    data=json.dumps(task, default=jsonable_encoder),
                    headers=headers,
                    timeout=3)
    time.sleep(2)
    result = BaseResult(task_id=task.id,
                        type=ResultType.DICOM,
                        status=ItemStatus.NEW,
                        filename=task.args["contrast"])
    requests.post(f"http://{EXAM_MANAGER_URI}/api/v1/exam/result",
                  data=json.dumps(result, default=jsonable_encoder),
                  headers=headers,
                  timeout=3)
    task.status = ItemStatus.FINISHED
    task.progress = 100
    requests.put(f"http://{EXAM_MANAGER_URI}/api/v1/exam/task/{task.id}",
                data=json.dumps(task, default=jsonable_encoder),
                headers=headers,
                timeout=3)


@router.post("/trigger_task/{task_id}/", tags=["WorkflowManager"])
async def trigger_task(task_id: str,
                       background_tasks: BackgroundTasks,
                       access_token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, Any]:
    """
    Endpoint to trigger a task in the orchestration engine.

    Args:
        task_id (str): The ID of the DAG to be triggered.

    Returns
    -------
        dict: A dictionary containing the response from the orchestration engine.
    """
    headers = {"Authorization": "Bearer " + access_token}
    get_task_response = requests.get(f"http://{EXAM_MANAGER_URI}/api/v1/exam/task/{task_id}", headers=headers, timeout=3)
    if get_task_response.status_code != 200:
        raise HTTPException(status_code=get_task_response.status_code, detail="Failed to fetch task with id=" + str(task_id))
    task_raw = get_task_response.json()
    print(f"\n>>>>>\nTriggering task: {task_raw}\n")
    if task_raw["task_type"] == "ACQUISITION":
        task = AcquisitionTaskOut(**task_raw)
    elif task_raw["task_type"] == "DAG":
        task = DAGTaskOut(**task_raw)
    else:
        raise TypeError("Invalid task type.")

    get_workflow_response = requests.get(f"http://{EXAM_MANAGER_URI}/api/v1/exam/workflow/{task.workflow_id}", headers=headers, timeout=3)
    if get_workflow_response.status_code != 200:
        raise HTTPException(status_code=get_workflow_response.status_code, detail="Failed to fetch workflow with id=" + str(task.workflow_id))
    workflow_raw = get_workflow_response.json()
    workflow = WorkflowOut(**workflow_raw)

    get_exam_response = requests.get(f"http://{EXAM_MANAGER_URI}/api/v1/exam/{workflow.exam_id}", headers=headers, timeout=3)
    if get_exam_response.status_code != 200:
        raise HTTPException(status_code=get_exam_response.status_code, detail="Failed to fetch exam with id=" + str(workflow.exam_id))
    exam_raw = get_exam_response.json()
    exam = ExamOut(**exam_raw)

    get_patient_response = requests.get(f"http://{PATIENT_MANAGER_URI}/api/v1/patient/{exam.patient_id}", headers=headers, timeout=3)
    if get_patient_response.status_code != 200:
        raise HTTPException(status_code=get_patient_response.status_code, detail="Failed to fetch patient with id=" + str(exam.patient_id))
    patient_raw = get_patient_response.json()
    patient = PatientOut(**patient_raw)

    print(f"\n>>>>>\nPatient: {patient.__dict__}\n")

    if task.task_type == TaskType.ACQUISITION:
        task.acquisition_limits = AcquisitionLimits(
            patient_height=patient.height,
            patient_weight=patient.weight,
            patient_gender=patient.sex,
            patient_age=calc_age_from_date(patient.birth_date)
        )
        print("Acquisition task: ", task)

    task.status = ItemStatus.STARTED
    requests.put(f"http://{EXAM_MANAGER_URI}/api/v1/exam/task/{task.id}",
                 data=json.dumps(task, default=jsonable_encoder),
                 headers=headers,
                 timeout=3)
    # could check response type here, but may be optional

    if task.task_type == TaskType.ACQUISITION:
        response = requests.post(
            f"http://{DEVICE_MANAGER_URI}/api/v1/device/start_scan_via_websocket",
            data=json.dumps(task, default=jsonable_encoder),
            headers=headers,
            timeout=3
        )
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error at starting device task.")
        print("Device task started successfully.")
        return {"status": "success", "data": "Device task started successfully."}
    elif task.task_type == TaskType.DAG:
        # background_tasks.add_task(simulate_reconstruction_task, task, headers)
        print("PROCESSING...")
        try:
            # Check if the file was successfully uploaded
            # if not os.path.exists(file_location):
            #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="File upload failed")
            # Define the callback endpoint
            callback_endpoint = "http://localhost:8443/api/v1/workflowmanager/results_ready/" #"http://workflow-manager:8000/api/v1/workflowmanager/results_ready/"

            # Trigger the Airflow DAG with the directory, file name, and callback endpoint as parameters
            dag_response = orchestration_engine.trigger_task(
                task.dag_id,
                conf={
                    "directory": "tmp",#directory,
                    "file_name": "file",#file.filename,
                    "workflow_manager_endpoint": callback_endpoint,
                    "user_token": access_token
                }
            )
            print(f"DAG triggered with response: {dag_response}")

            return {"message": "DAG triggered successfully", "data": dag_response}
        except Exception as e:
            logging.error(f"Failed to trigger DAG: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    else:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


def calc_age_from_date(birth_date: date) -> int:
    """Calculate age in years from a given birth date.

    Parameters
    ----------
    birth_date
        Date of birth

    Returns
    -------
        Age in years as int
    """
    today = date.today()
    age = today.year - birth_date.year
    # Adjust if birthday hasn't occurred yet this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


async def start_scan(task: AcquisitionTaskOut, access_token: str):
    """Load the device and sequence data from the database and start the scan for task types DEVICE_TASK_SIMULATOR and DEVICE_TASK_SDK.

    Parameters
    ----------
    task_type
        the type of the task to be started, must be one of DEVICE_TASK_SIMULATOR and DEVICE_TASK_SDK
    device_id
        the id of the device to start the task on
    sequence_id
        the id of the sequence to start
    record_id
        the record id
    acquisition_limits
        the acquisition limits as defined in the pydantic model
    sequence_parameters
        the sequence parameters
    access_token
        the access token of the current user

    Raises
    ------
        HttpException if something goes wrong.
    """
    headers = {"Authorization": "Bearer " + access_token}

    get_sequence_response = requests.get(f"http://{SEQUENCE_MANAGER_URI}/api/v1/mri/sequences/{task.sequence_id}",
                                         headers=headers,
                                         timeout=3)
    if get_sequence_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Could not retreive sequence for sequence_id:" + str(task.sequence_id))
    sequence_json = get_sequence_response.json()

    print("Sequence JSON:", sequence_json)

    # print("Post device task. URL:", url)
    # device_task_string = json.dumps(device_task, default=jsonable_encoder)
    # print("Post device task: device_task_string:", device_task_string)
    # response = requests.post(url, data=device_task_string, headers=headers, timeout=3)

    # if response.status_code != 200:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error at starting device task.")

    return {"status": "success", "data": "ok"}



@router.get("/tasks/", tags=["WorkflowManager"])
async def list_available_tasks():
    """Endpoint to list the available tasks from the orchestration engine.

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


@router.post("/process/{workflow_id}/", tags=["WorkflowManager"])
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
    # Fetch the workflow data from the exam manager service
    response = requests.get(f"http://{exam_manager_uri}/api/v1/exam/workflow/{workflow_id}", timeout=3)
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
    # job = ScanJob(
    #     job_id=task.id,
    #     sequence_id=task.args["sequence_id"],
    #     workflow_id=task.args["workflow_id"],
    #     device_id=task.destinations["device"],
    #     acquisition_limits=task.args["acquisition_limits"],
    #     sequence_parameters=task.args["sequence_parameters"]
    # )

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


@router.post("/upload_and_trigger/{dag_id}/", tags=["WorkflowManager"])
async def upload_and_trigger(dag_id: str,
                             access_token: Annotated[str, Depends(oauth2_scheme)],
                             file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload a file and trigger an Airflow DAG.

    Parameters
    ----------
    dag_id
        The ID of the DAG to be triggered.
    file, optional
        Data upload, e.g. reconstruction result, by default File(...)

    Returns
    -------
        dict: A dictionary containing a message and data.
    """
    if file.filename is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File has no file name.")
    try:
        # Define the file location in the shared data lake
        directory = f"/upload/{dag_id}"
        file_location = f"{data_lake_directory}{directory}/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)

        # Save the uploaded file
        with open(file_location, "wb") as f:
            f.write(await file.read())

        logging.info(f"File saved to {file_location}")

        # Check if the file was successfully uploaded
        if not os.path.exists(file_location):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="File upload failed")
        # Define the callback endpoint
        callback_endpoint = "http://workflow-manager:8000/api/v1/workflowmanager/results_ready/"

        # Trigger the Airflow DAG with the directory, file name, and callback endpoint as parameters
        response = orchestration_engine.trigger_task(
            dag_id,
            conf={
                "directory": directory,
                "file_name": file.filename,
                "workflow_manager_endpoint": callback_endpoint,
                "user_token": access_token
            }
        )
        logging.info(f"DAG triggered with response: {response}")

        return {"message": "File uploaded and DAG triggered successfully", "data": response}
    except Exception as e:
        logging.error(f"Failed to trigger DAG: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
