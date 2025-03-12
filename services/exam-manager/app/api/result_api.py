# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of result API endpoints accessible through swagger UI."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
# from fastapi.responses import FileResponse
from scanhub_libraries.models import BaseResult, ResultOut, User, ItemStatus
from scanhub_libraries.security import get_current_user
import os
import shutil


from app.dal import result_dal, task_dal

from app import LOG_CALL_DELIMITER

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found

result_router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@result_router.post("/result", response_model=ResultOut, status_code=201, tags=["results"])
async def create_result(payload: BaseResult, user: Annotated[User, Depends(get_current_user)]) -> ResultOut:
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
    print("payload:", payload)
    if payload.status != ItemStatus.NEW:
        raise HTTPException(status_code=400, detail="New result needs to have status NEW")
    if payload.task_id is not None:
        task_id = UUID(payload.task_id) if not isinstance(payload.task_id, UUID) else payload.task_id
        if not (task := await task_dal.get_task_data(task_id=task_id)):
            raise HTTPException(status_code=400, detail="Parent (task_id) does not exist.")
        if task.is_template:
            raise HTTPException(status_code=400, detail="Result parent (task) must not be a template.")
    if not (result := await result_dal.add_result_db(payload=payload)):
        raise HTTPException(status_code=404, detail="Could not create result")
    result = ResultOut(**result.__dict__)
    print("Result created: ", result)
    return result

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
        raise HTTPException(status_code=400, detail="Badly formed task_id.")
    if not (result := await result_dal.get_result_db(resuld_id=_id)):
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
async def update_result(result_id: UUID | str, payload: BaseResult,
                      user: Annotated[User, Depends(get_current_user)]) -> ResultOut:
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
    if payload.task_id is not None:
        task_id = UUID(payload.task_id) if not isinstance(payload.task_id, UUID) else payload.task_id
        if not await task_dal.get_task_data(task_id=task_id):
            raise HTTPException(status_code=400, detail="task_id must be an existing id.")

    _id = UUID(result_id) if not isinstance(result_id, UUID) else result_id
    if not (result_updated := await result_dal.update_result_db(result_id=_id, payload=payload)):
        message = "Could not update result, either because it does not exist, or for another reason."
        raise HTTPException(status_code=404, detail=message)
    print("Updated result: ", result_updated.__dict__)
    return ResultOut(**result_updated.__dict__)


@result_router.post("/dicom/{result_id}", status_code=200, tags=["results"])
async def upload_dicom(
    result_id: UUID | str, 
    file: UploadFile,
    user: Annotated[User, Depends(get_current_user)]
) -> None:
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("result_id:", result_id)
    if not (result := await result_dal.get_result_db(result_id)):
        message = f"Could not find result with ID {result_id}."
        raise HTTPException(status_code=404, detail=message)

    filename = result.filename if result.filename.endswith(".dcm") else result.filename + ".dcm"
    file_path = os.path.join(result.directory, filename)
    os.makedirs(result.directory, exist_ok=True)
    print("Saving dicom to: ", file_path)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
