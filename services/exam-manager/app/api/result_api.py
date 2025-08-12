# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of result API endpoints accessible through swagger UI."""
from pathlib import Path
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from scanhub_libraries.models import DAGTaskOut, ResultOut, SetResult, User
from scanhub_libraries.security import get_current_user

from app import LOG_CALL_DELIMITER
from app.api.task_api import get_task
from app.dal import result_dal, task_dal

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found

result_router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@result_router.post("/result", response_model=ResultOut, status_code=201, tags=["results"])
async def create_blank_result(task_id: str | UUID, user: Annotated[User, Depends(get_current_user)]) -> ResultOut:
    """Create a task result.

    Parameters
    ----------
    payload
        Result pydantic input model

    Returns
    -------
        Result pydantic output model

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("Creating blank result for task ID:", task_id)
    if task_id is not None:
        task_id = UUID(task_id) if not isinstance(task_id, UUID) else task_id
        if not (task := await task_dal.get_task_data(task_id=task_id)):
            raise HTTPException(status_code=400, detail="Parent (task_id) does not exist.")
        if task.is_template:
            raise HTTPException(status_code=400, detail="Result parent (task) must not be a template.")
    if not (result := await result_dal.add_blank_result_db(task_id=task_id)):
        raise HTTPException(status_code=404, detail="Could not create result")
    result_out = ResultOut(**result.__dict__)
    return result_out


@result_router.get(
    "/result/{result_id}",
    response_model=ResultOut,
    status_code=200,
    tags=["results"],
)
async def get_result(
    result_id: UUID | str, user: Annotated[User, Depends(get_current_user)]
) -> ResultOut:
    """Get an existing result.

    Parameters
    ----------
    result_id
        Id of the result to be returned

    Returns
    -------
        Result pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("task_id:", result_id)
    try:
        _id = UUID(result_id) if not isinstance(result_id, UUID) else result_id
    except ValueError:
        raise HTTPException(status_code=400, detail="Badly formed result_id.")
    if not (result := await result_dal.get_result_db(result_id=_id)):
        raise HTTPException(status_code=404, detail="Result not found")
    return ResultOut(**result.__dict__)


@result_router.get(
    "/result/all/{task_id}",
    response_model=list[ResultOut],
    status_code=200,
    tags=["results"],
)
async def get_all_task_results(
    task_id: UUID | str,
    user: Annotated[User, Depends(get_current_user)]) -> list[ResultOut]:
    """Get all existing results of a certain task.

    Parameters
    ----------
    task_id
        Id of parental task

    Returns
    -------
        List of task pydantic output model
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("task_id:", task_id)
    _id = UUID(task_id) if not isinstance(task_id, UUID) else task_id
    if not (tasks := await result_dal.get_all_results_db(task_id=_id)):
        # Don't raise exception here, list might be empty.
        return []
    result = [ResultOut(**task.__dict__) for task in tasks]
    print("List of tasks: ", result)
    return result


@result_router.delete("/result/{result_id}", response_model={}, status_code=204, tags=["results"])
async def delete_result(result_id: UUID | str, user: Annotated[User, Depends(get_current_user)]) -> None:
    """Delete a task.

    Parameters
    ----------
    task_id
        Id of the task to be deleted

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("result_id:", result_id)
    _id = UUID(result_id) if not isinstance(result_id, UUID) else result_id
    if not await result_dal.delete_result_db(result_id=_id):
        message = "Could not delete result, either because it does not exist, or for another reason."
        raise HTTPException(status_code=404, detail=message)


@result_router.put("/result/{result_id}", response_model=ResultOut, status_code=200, tags=["results"])
async def set_result(
    result_id: UUID | str,
    payload: SetResult,
    user: Annotated[User, Depends(get_current_user)]
) -> ResultOut:
    """Update an existing result.

    Parameters
    ----------
    result_id
        Id of the result to be updated
    payload
        Result pydantic base model/dict
        If this is the pydantic ResultBase model, only fields in the base model can be updated.

    Returns
    -------
        Task pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("result_id:", result_id)
    _id = UUID(result_id) if not isinstance(result_id, UUID) else result_id
    if not (result_updated := await result_dal.update_result_db(result_id=_id, payload=payload)):
        message = "Could not update result, either because it does not exist, or for another reason."
        raise HTTPException(status_code=404, detail=message)
    print("Updated result: ", result_updated.__dict__)
    return ResultOut(**result_updated.__dict__)


@result_router.get("/dicom/{task_id}", response_class=FileResponse, status_code=200, tags=["results"])
async def get_dicom(task_id: str | UUID, user: Annotated[User, Depends(get_current_user)]) -> FileResponse:
    """Get DICOM file of a task result."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("task_id:", task_id)

    # Get task and perform checks
    task_id = UUID(task_id) if not isinstance(task_id, UUID) else task_id
    if not (task := await get_task(task_id=task_id, user=user)):
        raise HTTPException(status_code=400, detail="Task ID does not exist.")
    if task.is_template:
        raise HTTPException(status_code=400, detail="Task is not an instance.")
    if not isinstance(task, DAGTaskOut):
        raise HTTPException(status_code=400, detail="Task is not a DAG task, dicom does not exist.")
    if not task.results:
        raise HTTPException(status_code=404, detail="Task has no results, dicom does not exist.")

    # Retrieve the latest result
    result = sorted(task.results, key=lambda r: r.datetime_created, reverse=True)[0]
    # Define the path to the DICOM file
    data_path = (Path("/data") / str(task.workflow_id) / f"{str(result.id)}").resolve()
    if not data_path.exists():
        raise HTTPException(status_code=404, detail=f"Could not find result folder for result ID: {result.id}.")

    dicom_file = sorted(data_path.rglob("*.dcm"))[0]    # Get the first DICOM file found
    # TODO: Should return all dicom files from result folder
    if not dicom_file.is_file():
        raise HTTPException(status_code=404, detail=f"Dicom is not a file: {dicom_file}.")

    print(f"Path to dicom file: {dicom_file}")

    # FileResponse in Starlette supports range requests by default
    resp = FileResponse(
        path=str(dicom_file),
        media_type="application/dicom",
    )

    # Make sure browsers/viewers treat it as inline binary (not forced download)
    resp.headers["Content-Disposition"] = f'inline; filename="{str(dicom_file)}"'
    # Explicitly advertise range support (useful for some viewers)
    resp.headers["Accept-Ranges"] = "bytes"
    # Optional: avoid caching if your data is dynamic or protected
    # resp.headers["Cache-Control"] = "no-store"

    return resp
