"""
Handler for exam requests.

This module defines functions to interact with the exam manager service,
including fetching tasks, sequences, and results. It provides a way to
create and update acquisition tasks and results, ensuring that the data
is properly formatted and authenticated.

Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
"""
import json
from uuid import UUID

import requests
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from scanhub_libraries.models import AcquisitionTaskOut, DAGTaskOut, ResultOut, SetResult, WorkflowOut

TASK_URI = "http://exam-manager:8000/api/v1/exam/task"
RESULT_URI = "http://exam-manager:8000/api/v1/exam/result"
WORKFLOW_URI = "http://exam-manager:8000/api/v1/exam"


def get_task(task_id: str | UUID, user_access_token: str) -> AcquisitionTaskOut | DAGTaskOut:
    """
    Fetch acquisition task by ID from the exam manager service.

    Args
    ----
        task_id (str | UUID): The unique identifier of the task to retrieve.
        user_access_token (str): The user's access token for authentication.

    Returns
    -------
        AcquisitionTaskOut | None: The acquisition task object if found and valid.

    Raises
    ------
        HTTPException: If the task is not found (404) or is not an acquisition task (400).
    """
    headers = {"Authorization": "Bearer " + user_access_token}
    _id = str(task_id) if isinstance(task_id, UUID) else task_id
    get_task_response = requests.get(f"{TASK_URI}/{_id}", headers=headers, timeout=3)

    if get_task_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Task not found")

    task_raw = get_task_response.json()

    task: AcquisitionTaskOut | DAGTaskOut
    if task_raw["task_type"] == "ACQUISITION":
        task = AcquisitionTaskOut(**task_raw)
    elif task_raw["task_type"] == "DAG":
        task = DAGTaskOut(**task_raw)
    else:
        raise HTTPException(status_code=400, detail="Task has not a valid type.")
    return task


def set_task(
    task_id: str | UUID,
    payload: AcquisitionTaskOut | DAGTaskOut,
    user_access_token: str,
) -> AcquisitionTaskOut | DAGTaskOut:
    """
    Update an acquisition task on the task service with the provided payload.

    Parameters
    ----------
    task_id : str | UUID
        The unique identifier of the task to update.
    payload : AcquisitionTaskOut
        The updated task data to send to the task service.
    user_access_token : str
        The access token used for authorization with the task service.

    Returns
    -------
    AcquisitionTaskOut
        The updated task object returned from the task service.

    Raises
    ------
    HTTPException
        If the task update fails (e.g. non-200 response from the task service).
    """
    _id = str(task_id) if isinstance(task_id, UUID) else task_id
    update_task_response = requests.put(
        f"{TASK_URI}/{_id}",
        data=json.dumps(payload, default=jsonable_encoder),
        headers={"Authorization": "Bearer " + user_access_token},
        timeout=3,
    )
    if update_task_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error updating task")
    updated_task = update_task_response.json()
    if updated_task["task_type"] == "ACQUISITION":
        return AcquisitionTaskOut(**updated_task)
    elif updated_task["task_type"] == "DAG":
        return DAGTaskOut(**updated_task)
    else:
        raise HTTPException(status_code=400, detail="Invalid task type")


def create_blank_result(task_id: str, user_access_token: str) -> ResultOut:
    """
    Create a blank result in the exam manager service.

    Returns
    -------
        ResultOut: The created blank result object.

    Raises
    ------
        HTTPException: If the result creation fails (status code not 201).
    """
    headers = {"Authorization": "Bearer " + user_access_token}
    blank_result_response = requests.post(
        RESULT_URI, params={"task_id": task_id}, headers=headers, timeout=3
    )
    if blank_result_response.status_code != 201:
        raise HTTPException(status_code=404, detail="Could not create blank result.")
    return ResultOut(**blank_result_response.json())


def set_result(result_id: str | UUID, payload: SetResult | ResultOut, user_access_token: str) -> ResultOut:
    """
    Update a result in the exam manager service.

    Args
    ----
        result_id (str): The unique identifier of the result to update.
        payload (SetResult): The data to update the result with.
        user_access_token (str): The user's access token for authentication.

    Returns
    -------
        ResultOut: The updated result object.

    Raises
    ------
        HTTPException: If the result update fails (status code not 200).
    """
    headers = {"Authorization": "Bearer " + user_access_token}
    _id = str(result_id) if isinstance(result_id, UUID) else result_id
    update_result_response = requests.put(
        f"{RESULT_URI}/{_id}",
        data=json.dumps(payload, default=jsonable_encoder),
        headers=headers,
        timeout=3,
    )
    if update_result_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error updating result")
    return ResultOut(**update_result_response.json())


def get_result(result_id: str | UUID, user_access_token: str) -> ResultOut:
    """
    Fetch a result by ID from the exam manager service.

    Args
    ----
        result_id (str): The unique identifier of the result to retrieve.
        user_access_token (str): The user's access token for authentication.

    Returns
    -------
        ResultOut: The result object if found.

    Raises
    ------
        HTTPException: If the result is not found (404).
    """
    headers = {"Authorization": "Bearer " + user_access_token}
    _id = str(result_id) if isinstance(result_id, UUID) else result_id
    response = requests.get(f"{RESULT_URI}/{_id}", headers=headers, timeout=3)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Result not found")
    return ResultOut(**response.json())


def get_exam_id(workflow_id: str, user_access_token: str) -> str:
    """
    Fetch acquisition task by ID from the exam manager service.

    Args
    ----
        task_id (str): The unique identifier of the task to retrieve.
        user_access_token (str): The user's access token for authentication.

    Returns
    -------
        AcquisitionTaskOut | None: The acquisition task object if found and valid.

    Raises
    ------
        HTTPException: If the task is not found (404) or is not an acquisition task (400).
    """
    headers = {"Authorization": "Bearer " + user_access_token}
    response = requests.get(f"{WORKFLOW_URI}/{workflow_id}", headers=headers, timeout=3)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Task not found")
    workflow = WorkflowOut(**response.json())
    return str(workflow.exam_id)
