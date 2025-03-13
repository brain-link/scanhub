# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow manager endpoints."""
import datetime
import json
import time
import logging
import operator
import os
from typing import Annotated, Any, Dict
from uuid import UUID

import requests
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from scanhub_libraries.models import (
    AcquisitionLimits,
    Commands,
    DeviceTask,
    ExamOut,
    ItemStatus,
    ParametrizedSequence,
    PatientOut,
    SequenceParameters,
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
    print('Simulate reconstruction task.')
    for percentage in [25, 50, 75, 100]:
        time.sleep(2)
        task.progress = percentage
        if percentage == 100:
            task.status = ItemStatus.FINISHED
        requests.put(f"http://{EXAM_MANAGER_URI}/api/v1/exam/task/{task.id}",
                    data=json.dumps(task, default=jsonable_encoder),
                    headers=headers)


@router.post("/trigger_task/{task_id}/", tags=["WorkflowManager"])
async def trigger_task(task_id: str,
                       backgroundTasks: BackgroundTasks,
                       access_token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, Any]:
    """
    Endpoint to trigger a task in the orchestration engine.

    Args:
        task_id (str): The ID of the DAG to be triggered.

    Returns
    -------
        dict: A dictionary containing the response from the orchestration engine.
    """
    print(f"Triggering task: {task_id}")

    headers = {"Authorization": "Bearer " + access_token}
    get_task_response = requests.get(f"http://{EXAM_MANAGER_URI}/api/v1/exam/task/{task_id}", headers=headers)
    if get_task_response.status_code != 200:
        raise HTTPException(status_code=get_task_response.status_code, detail="Failed to fetch task with id=" + str(task_id))
    task_raw = get_task_response.json()
    task = TaskOut(**task_raw)
    print("Task:")
    print("    workflow_id:     ", task.workflow_id)
    print("    name:            ", task.name)
    print("    description:     ", task.description)
    print("    comment:         ", task.comment)
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
    print("    status:          ", task.status)
    print("    is_template:     ", task.is_template)
    print("    id:              ", task.id)
    print("    creator:         ", task.creator)
    print("    datetime_created:", task.datetime_created)
    print("    datetime_updated:", task.datetime_updated)
    print()

    get_workflow_response = requests.get(f"http://{EXAM_MANAGER_URI}/api/v1/exam/workflow/{task.workflow_id}", headers=headers)
    if get_workflow_response.status_code != 200:
        raise HTTPException(status_code=get_workflow_response.status_code, detail="Failed to fetch workflow with id=" + str(task.workflow_id))
    workflow_raw = get_workflow_response.json()
    workflow = WorkflowOut(**workflow_raw)
    print("Workflow:")
    print("    exam_id:         ", workflow.exam_id)
    print("    name:            ", workflow.name)
    print("    description:     ", workflow.description)
    print("    comment:         ", workflow.comment)
    print("    status:          ", workflow.status)
    print("    is_template:     ", workflow.is_template)
    print("    id:              ", workflow.id)
    print("    creator:         ", workflow.creator)
    print("    datetime_created:", workflow.datetime_created)
    print("    datetime_updated:", workflow.datetime_updated)
    print()
    # print workflow.tasks

    get_exam_response = requests.get(f"http://{EXAM_MANAGER_URI}/api/v1/exam/{workflow.exam_id}", headers=headers)
    if get_exam_response.status_code != 200:
        raise HTTPException(status_code=get_exam_response.status_code, detail="Failed to fetch exam with id=" + str(workflow.exam_id))
    exam_raw = get_exam_response.json()
    exam = ExamOut(**exam_raw)
    print("Exam:")
    print("    patient_id:          ", exam.patient_id)
    print("    name:                ", exam.name)
    print("    description:         ", exam.description)
    print("    indication:          ", exam.indication)
    print("    patient_height_cm:   ", exam.patient_height_cm)
    print("    patient_weight_kg:   ", exam.patient_weight_kg)
    print("    comment:             ", exam.comment)
    print("    status:              ", exam.status)
    print("    is_template:         ", exam.is_template)
    print("    id:                  ", exam.id)
    print("    creator:             ", exam.creator)
    print("    datetime_created:    ", exam.datetime_created)
    print("    datetime_updated:    ", exam.datetime_updated)
    print()
    # print exam.workflows

    get_patient_response = requests.get(f"http://{PATIENT_MANAGER_URI}/api/v1/patient/{exam.patient_id}", headers=headers)
    if get_patient_response.status_code != 200:
        raise HTTPException(status_code=get_patient_response.status_code, detail="Failed to fetch patient with id=" + str(exam.patient_id))
    patient_raw = get_patient_response.json()
    patient = PatientOut(**patient_raw)
    print("Patient:")
    print("    first_name:          ", patient.first_name)
    print("    last_name:           ", patient.last_name)
    print("    birth_date:          ", patient.birth_date)
    print("    sex:                 ", patient.sex)
    print("    issuer:              ", patient.issuer)
    print("    status:              ", patient.status)
    print("    comment:             ", patient.comment)
    print("    patient_id:          ", patient.patient_id)
    print("    datetime_created:    ", patient.datetime_created)
    print("    datetime_updated:    ", patient.datetime_updated)
    print()

    task.status = ItemStatus.STARTED
    requests.put(f"http://{EXAM_MANAGER_URI}/api/v1/exam/task/{task.id}",
                 data=json.dumps(task, default=jsonable_encoder),
                 headers=headers)
    # could check response type here, but may be optional

    if task.type == TaskType.DEVICE_TASK_SDK:
        response = await start_scan(task_type=task.type,
                           device_id=task.args["device_id"],
                           sequence_id=task.args["sequence_id"],
                           record_id=task.id,
                           acquisition_limits={
                               "patient_height": exam.patient_height_cm,
                               "patient_weight": exam.patient_weight_kg,
                               "patient_gender": patient.sex,
                               "patient_age": calculate_age(patient.birth_date),
                           },
                           sequence_parameters=json.loads(task.args["sequence_parameters"]),
                           access_token=access_token)
        return {"status": "success", "data": "ok"}
    elif task.type == TaskType.RECONSTRUCTION_TASK:
        backgroundTasks.add_task(simulate_reconstruction_task, task, headers)
        return {"status": "success", "data": "ok"}

        # try:
        #     response = orchestration_engine.trigger_task(task_id)
        #     return {"status": "success", "data": response}
        # except Exception as e:
        #     logging.error(f"Failed to trigger task: {e}")
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


def calculate_age(birth_date):
    """Calculate age in years from birth date.

    Parameters
    ----------
    birth_date
        date of birth as datetime.date object

    Returns
    -------
        Age in years as integer
    """
    today = datetime.date.today()
    age = today.year - birth_date.year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age


async def start_scan(task_type: str,
                     device_id: str,
                     sequence_id: str,
                     record_id: str,
                     acquisition_limits: AcquisitionLimits,
                     sequence_parameters: SequenceParameters,
                     access_token: str):
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

    get_sequence_response = requests.get(f"http://{SEQUENCE_MANAGER_URI}/api/v1/mri/sequences/{sequence_id}",
                                         headers=headers)
    if get_sequence_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Could not retreive sequence for sequence_id:" + str(sequence_id))
    sequence_json = get_sequence_response.json()

    print("Sequence JSON:", sequence_json)

    parametrized_sequence = ParametrizedSequence(
        acquisition_limits=acquisition_limits,
        sequence_parameters=sequence_parameters,
        sequence=json.dumps(sequence_json),
    )

    device_task = DeviceTask(
        device_id=device_id,
        record_id=record_id,
        command=Commands.START,
        parametrized_sequence=parametrized_sequence,
        user_access_token=access_token
    )

    print("Device task:", device_task)

    if task_type == "DEVICE_TASK_SIMULATOR":
        raise RuntimeError("Not implemented at the moment.")
        # device_ip = await device_location_request(device_id, access_token)
        # print("Device ip: ", device_ip)
        # url = f"http://{device_ip}/api/start-scan"
    elif task_type == "DEVICE_TASK_SDK":
        url = f"http://{DEVICE_MANAGER_URI}/api/v1/device/start_scan_via_websocket"
    else:
        raise RuntimeError("Task type must be DEVICE_TASK_SIMULATOR or DEVICE_TASK_SDK")

    print("Post device task. URL:", url)
    device_task_string = json.dumps(device_task, default=jsonable_encoder)
    print("Post device task: device_task_string:", device_task_string)
    response = requests.post(url, data=device_task_string, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error at starting device task.")

    return response



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
    response = requests.get(f"http://{exam_manager_uri}/api/v1/exam/workflow/{workflow_id}")
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

