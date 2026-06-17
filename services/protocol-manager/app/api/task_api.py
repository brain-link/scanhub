# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of task API endpoints."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from scanhub_libraries.models import AcquisitionTaskOut, BaseAcquisitionTask, ItemStatus, User
from scanhub_libraries.security import get_current_user
from scanhub_libraries.utils import ensure_uuid

from app import LOG_CALL_DELIMITER
from app.dal import protocol_dal
from app.dal import task_dal
from app.tools.helper import get_task_out

task_router = APIRouter(dependencies=[Depends(get_current_user)])


class TaskReorder(BaseModel):
    """Task reorder model."""

    task_ids: list[UUID]


@task_router.post("/task/new", response_model=AcquisitionTaskOut, status_code=201, tags=["tasks"], operation_id="create_task")
async def create_task(
    payload: BaseAcquisitionTask,
    user: Annotated[User, Depends(get_current_user)],
) -> AcquisitionTaskOut:
    """Create a new acquisition task."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    if payload.status != ItemStatus.NEW:
        raise HTTPException(status_code=400, detail="New task needs to have status NEW")
    if (protocol_id := ensure_uuid(payload.protocol_id)) is not None:
        if not (protocol := await protocol_dal.get_protocol_data(protocol_id=protocol_id)):
            raise HTTPException(status_code=400, detail="protocol_id must be an existing id.")
        if protocol.is_template != payload.is_template:
            raise HTTPException(
                status_code=400,
                detail="Invalid link to protocol. Instance needs to refer to instance, template to template.",
            )
    if payload.is_template is False and payload.protocol_id is None:
        raise HTTPException(status_code=400, detail="Task instance needs protocol_id.")
    if not (task := await task_dal.add_task_data(payload=payload, creator=user.username)):
        raise HTTPException(status_code=404, detail="Could not create task")
    return await get_task_out(data=task)


@task_router.post("/task", response_model=AcquisitionTaskOut, status_code=201, tags=["tasks"], operation_id="create_task_from_template")
async def create_task_from_template(
    protocol_id: UUID,
    template_id: UUID,
    new_task_is_template: bool,
    user: Annotated[User, Depends(get_current_user)],
) -> AcquisitionTaskOut:
    """Create a new acquisition task from a template."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    if not (template := await task_dal.get_task_data(task_id=template_id)):
        raise HTTPException(status_code=404, detail="Task template not found")
    if not template.is_template:
        raise HTTPException(status_code=400, detail="Provided task is not a template.")
    new_task = BaseAcquisitionTask(**template.__dict__)
    new_task.is_template = new_task_is_template
    new_task.protocol_id = protocol_id
    if not (protocol := await protocol_dal.get_protocol_data(protocol_id=protocol_id)):
        raise HTTPException(status_code=400, detail="protocol_id must be an existing id.")
    if protocol.is_template != new_task_is_template:
        raise HTTPException(
            status_code=400,
            detail="Invalid link to protocol. Instance needs to refer to instance, template to template.",
        )
    if not (task := await task_dal.add_task_data(payload=new_task, creator=user.username)):
        raise HTTPException(status_code=404, detail="Could not create task.")
    return await get_task_out(data=task)


@task_router.get("/task/{task_id}", response_model=AcquisitionTaskOut, status_code=200, tags=["tasks"], operation_id="get_task")
async def get_task(
    task_id: UUID | str, user: Annotated[User, Depends(get_current_user)]
) -> AcquisitionTaskOut:
    """Get an existing task."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    try:
        _id = UUID(task_id) if not isinstance(task_id, UUID) else task_id
    except ValueError:
        raise HTTPException(status_code=400, detail="Badly formed task_id.")
    if not (task := await task_dal.get_task_data(task_id=_id)):
        raise HTTPException(status_code=404, detail="Task not found")
    return await get_task_out(data=task)


@task_router.get("/task/all/{protocol_id}", response_model=list[AcquisitionTaskOut], status_code=200, tags=["tasks"], operation_id="get_all_protocol_tasks")
async def get_all_protocol_tasks(
    protocol_id: UUID | str,
    user: Annotated[User, Depends(get_current_user)],
) -> list[AcquisitionTaskOut]:
    """Get all tasks of a protocol."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    _id = UUID(protocol_id) if not isinstance(protocol_id, UUID) else protocol_id
    if not (tasks := await task_dal.get_all_task_data(protocol_id=_id)):
        return []
    return [await get_task_out(data=task) for task in tasks]


@task_router.get("/task/templates/all", response_model=list[AcquisitionTaskOut], status_code=200, tags=["tasks"], operation_id="get_all_task_templates")
async def get_all_task_templates(
    user: Annotated[User, Depends(get_current_user)],
) -> list[AcquisitionTaskOut]:
    """Get all task templates."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    if not (tasks := await task_dal.get_all_task_template_data()):
        return []
    return [await get_task_out(data=task) for task in tasks]


@task_router.delete("/task/{task_id}", response_model=None, status_code=204, tags=["tasks"], operation_id="delete_task")
async def delete_task(task_id: UUID | str, user: Annotated[User, Depends(get_current_user)]) -> None:
    """Delete a task."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    _id = UUID(task_id) if not isinstance(task_id, UUID) else task_id
    if not await task_dal.delete_task_data(task_id=_id):
        raise HTTPException(status_code=404, detail="Could not delete task.")


@task_router.put("/task/reorder", response_model=None, status_code=204, tags=["tasks"], operation_id="reorder_tasks")
async def reorder_tasks(
    payload: TaskReorder,
    user: Annotated[User, Depends(get_current_user)],
) -> None:
    """Reorder tasks by updating their position."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    if not await task_dal.reorder_tasks_data(task_ids=payload.task_ids):
        raise HTTPException(status_code=404, detail="Could not reorder tasks")


@task_router.put("/task/{task_id}", response_model=AcquisitionTaskOut, status_code=200, tags=["tasks"], operation_id="update_task")
async def update_task(
    task_id: UUID | str,
    payload: BaseAcquisitionTask,
    user: Annotated[User, Depends(get_current_user)],
) -> AcquisitionTaskOut:
    """Update an existing task."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    if (protocol_id := ensure_uuid(payload.protocol_id)) is not None:
        if not (protocol := await protocol_dal.get_protocol_data(protocol_id=protocol_id)):
            raise HTTPException(status_code=400, detail="protocol_id must be an existing id.")
        if protocol.is_template != payload.is_template:
            raise HTTPException(
                status_code=400,
                detail="Invalid link to protocol. Instance needs to refer to instance, template to template.",
            )
    if payload.is_template is False and payload.protocol_id is None:
        raise HTTPException(status_code=400, detail="Task instance needs protocol_id.")
    _id = UUID(task_id) if not isinstance(task_id, UUID) else task_id
    if not (task_updated := await task_dal.update_task_data(task_id=_id, payload=payload)):
        raise HTTPException(status_code=404, detail="Could not update task.")
    return await get_task_out(data=task_updated)


@task_router.put("/task/{task_id}/status", response_model=AcquisitionTaskOut, status_code=200, tags=["tasks"], operation_id="update_task_status")
async def update_task_status(
    task_id: UUID | str,
    status: str,
    user: Annotated[User, Depends(get_current_user)],
) -> AcquisitionTaskOut:
    """Update only the status of a task (called by Dagster sensors)."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    _id = UUID(task_id) if not isinstance(task_id, UUID) else task_id
    if not (task := await task_dal.update_task_status(task_id=_id, status=status)):
        raise HTTPException(status_code=404, detail="Task not found.")
    return await get_task_out(data=task)
