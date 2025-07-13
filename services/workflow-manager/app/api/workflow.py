# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""
Workflow manager endpoints.

TODO: How to handle tasks, and where to trigger the device task?
- There should be one endpoint for task, workflow and exam
- The endpoint processes the list, i.e. all the contained tasks
- Does it help to store an index with each task?

"""
import json
import logging
import os
from typing import Annotated, Any, Dict

import requests
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from scanhub_libraries.models import (
    AcquisitionLimits,
    AcquisitionTaskOut,
    DAGTaskOut,
    ExamOut,
    ItemStatus,
    PatientOut,
    TaskType,
    WorkflowOut,
)
from scanhub_libraries.security import get_current_user
from scanhub_libraries.utils import calc_age_from_date

from .orchestration_engine import OrchestrationEngine

router = APIRouter(dependencies=[Depends(get_current_user)])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

orchestration_engine = OrchestrationEngine()

# Define the URIs for the different managers
EXAM_MANAGER_URI = "exam-manager:8000"
PATIENT_MANAGER_URI = "patient-manager:8100"
DEVICE_MANAGER_URI = "device-manager:8000"


router = APIRouter(dependencies=[Depends(get_current_user)])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
orchestration_engine = OrchestrationEngine()


# Read the DATA_LAKE_DIRECTORY environment variable
data_lake_directory = os.getenv('DATA_LAKE_DIRECTORY', '/default/path/if/not/set')


@router.post("/trigger_task/{task_id}/", tags=["WorkflowManager"])
async def trigger_task(task_id: str,
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
    task: AcquisitionTaskOut | DAGTaskOut
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
            patient_height=int(patient.height),
            patient_weight=int(patient.weight),
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
        print("Triggering DAG...")
        try:
            # Check if the file was successfully uploaded
            # if not os.path.exists(file_location):
            #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="File upload failed")
            # Define the callback endpoint
            callback_endpoint = "http://localhost:8443/api/v1/workflowmanager/results_ready/" #"http://workflow-manager:8000/api/v1/workflowmanager/results_ready/"

            # Update the task status to IN_PROGRESS
            # TBD task.status = ItemStatus.IN_PROGRESS

            if not task.results:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No results found for the task.")

            sorted_results = sorted(task.results, key=lambda r: r.datetime_created, reverse=True)
            latest_result = sorted_results[0]

            # Trigger the Airflow DAG with the directory, file name, and callback endpoint as parameters
            dag_response = orchestration_engine.trigger_task(
                task.dag_id,
                conf={
                    "directory": latest_result.directory or "tmp",
                    "file_name": latest_result.filename or "test.py",
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


@router.post("/results_ready/{dag_id}/", tags=["WorkflowManager"])
async def callback_results_ready(dag_id: str, access_token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, Any]:
    """
    Notify that results are ready via callback endpoint.

    Args:
        dag_id (str): The ID of the DAG.
        access_token (str): The access token for authentication.

    Returns
    -------
        dict: A dictionary containing a success message.
    """
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.post(
        f"http://{EXAM_MANAGER_URI}/api/v1/exam/workflow/{dag_id}/results_ready",
        headers=headers,
        timeout=3  # Added timeout to fix S113
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to notify results ready.")
    return {"message": "Results ready notification sent successfully."}


# Test endpoint to upload a file and trigger a DAG
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
