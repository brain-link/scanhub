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
from pathlib import Path
from typing import Annotated, Any
from uuid import UUID

import requests
from dagster import RunConfig
from dagster_graphql import DagsterGraphQLClient
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from scanhub_libraries.models import (
    AcquisitionLimits,
    DAGTaskOut,
    ExamOut,
    ItemStatus,
    PatientOut,
    ResultType,
    SetResult,
    TaskType,
    WorkflowOut,
)
from scanhub_libraries.resources import SCANHUB_RESOURCE_KEY, JobConfigResource
from scanhub_libraries.security import get_current_user
from scanhub_libraries.utils import calc_age_from_date

from app.api.dagster_queries import list_dagster_jobs, parse_job_id
from app.api.scanhub_requests import create_blank_result, get_task, set_result, set_task

# Define the URIs for the different managers
EXAM_MANAGER_URI = "exam-manager:8000"
PATIENT_MANAGER_URI = "patient-manager:8100"
DEVICE_MANAGER_URI = "device-manager:8000"
DATA_LAKE_DIR = os.getenv("DATA_LAKE_DIRECTORY")
if DATA_LAKE_DIR is None:   # ensure that DATA_LAKE_DIR is set
    raise OSError("Missing `DATA_LAKE_DIRECTORY` environment variable.")


# Define dagster graphQL client
dg_client = DagsterGraphQLClient("dagster-dagit:3000/dagit", use_https=False)
# Define the API router
router = APIRouter(dependencies=[Depends(get_current_user)])
# Define OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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

    task = get_task(task_id, access_token)
    print(f"\n>>>>>\nTriggering task: {task.model_dump_json()}\n")


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
    set_task(task.id, task, access_token)

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
            # Get input, i.e. latest result of input task
            if not task.input_id:
                print("Missing task input ID")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DAG task input does not exist.")
            if not (input_task := get_task(str(task.input_id), access_token)).results:
                print("Selected input task does not have any results yet.")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No results found for input task {input_task.id}.")
            latest_result_in = sorted(input_task.results, key=lambda r: r.datetime_created, reverse=True)[0]

            # Update the task status to IN_PROGRESS
            task.status = ItemStatus.INPROGRESS
            set_task(task.id, task, access_token)

            # Use internal url and http (not https and port 8443) because callback endpoint is requested from another docker container
            callback_endpoint = f"http://workflow-manager:8000/api/v1/workflowmanager/result_ready/{task.id}"

            # Create blank result
            new_result_out = create_blank_result(task_id, access_token)
            # Update result info with created ID
            new_result_out = set_result(
                result_id=str(new_result_out.id),
                payload=SetResult(
                    type=ResultType.DICOM,
                    directory=str(Path(latest_result_in.directory) / str(new_result_out.id)),
                    filename="*.dcm",
                ),
                user_access_token=access_token,
            )

            print(f"Created new result: {new_result_out.model_dump_json()}")

            # Trigger dagster job
            job_name, repository, location = parse_job_id(task.dag_id)
            print(f"Triggering job: {job_name} in repository: {repository} at location: {location}")
            new_run_id = dg_client.submit_job_execution(
                job_name=job_name,
                repository_location_name=location,
                repository_name=repository,
                run_config=RunConfig(resources={
                    SCANHUB_RESOURCE_KEY: JobConfigResource(
                        callback_url=callback_endpoint,
                        user_access_token=access_token,
                        input_file=str(Path(latest_result_in.directory) / latest_result_in.filename),
                        output_dir=new_result_out.directory,
                    ),
                }),
            )
            print(f"DAG triggered, new run ID: {new_run_id}")

            return {"message": "DAG triggered successfully", "data": new_run_id}
        except Exception as e:
            logging.error(f"Failed to trigger DAG: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    else:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.post("/result_ready/{task_id}", tags=["WorkflowManager"])
async def callback_results_ready(task_id: UUID | str, access_token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, Any]:
    """
    Notify that results are ready via callback endpoint.

    Args:
        dag_id (str): The ID of the DAG.
        access_token (str): The access token for authentication.

    Returns
    -------
        dict: A dictionary containing a success message.
    """
    task = get_task(task_id, access_token)
    if not isinstance(task, DAGTaskOut):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Result ready callback received invalid task_id: {task.id}",
        )
    print("CALLBACK: Result ready for DAG ID ", task.dag_id)
    task.status = ItemStatus.FINISHED
    set_task(task.id, task, access_token)
    return {"message": "Results ready notification sent successfully."}


# Test endpoint to upload a file and trigger a DAG
@router.get("/tasks/", tags=["WorkflowManager"])
async def list_available_tasks():
    """Endpoint to list the available tasks from the orchestration engine.

    Returns
    -------
        dict: A dictionary containing the list of available dagster jobs.
    """
    return list_dagster_jobs()
