# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Data acess layer (DAL) between fastapi endpoint and sql database."""

from uuid import UUID

from scanhub_libraries.models import BaseTask
from sqlalchemy.engine import Result
from sqlalchemy.future import select

from app.db.postgres import Task, async_session


async def add_task_data(payload: BaseTask, creator) -> Task:
    """Add new task to database.

    Parameters
    ----------
    payload
        Task pydantic base model
    creator
        The username/id of the user who creats this task

    Returns
    -------
        Database orm model of created task
    """
    new_task = Task(**payload.dict(), creator=creator)
    async with async_session() as session:
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
    return new_task


async def get_task_data(task_id: UUID) -> (Task | None):
    """Get task by id.

    Parameters
    ----------
    task_id
        Id of the requested task

    Returns
    -------
        Database orm model with data of requested task
    """
    async with async_session() as session:
        return await session.get(Task, task_id)


async def get_all_task_data(workflow_id: UUID) -> list[Task]:
    """Get a list of all tasks assigned to a certain workflow.

    Parameters
    ----------
    workflow_id
        Id of the parent workflow entry, tasks are assigned to

    Returns
    -------
        List of task data base orm models
    """
    async with async_session() as session:
        result: Result = await session.execute(select(Task).where(Task.workflow_id == workflow_id))
        return list(result.scalars().all())


async def get_all_task_template_data() -> list[Task]:
    """Get a list of all tasks assigned to a certain workflow.

    Parameters
    ----------
    workflow_id
        Id of the parent workflow entry, tasks are assigned to

    Returns
    -------
        List of task data base orm models
    """
    async with async_session() as session:
        result: Result = await session.execute(select(Task).where(Task.is_template))
        return list(result.scalars().all())


async def delete_task_data(task_id: UUID) -> bool:
    """Delete task by id.

    Parameters
    ----------
    task_id
        Id of the task to be deleted

    Returns
    -------
        Success of deletion
    """
    async with async_session() as session:
        if task := await session.get(Task, task_id):
            await session.delete(task)
            await session.commit()
            return True
        return False


async def update_task_data(task_id: UUID, payload: BaseTask) -> (Task | None):
    """Update existing task in database.

    Parameters
    ----------
    task_id
        Id of the task to be updateed
    payload
        Task pydantic base model with data to be updated

    Returns
    -------
        Database orm model of updated task
    """
    async with async_session() as session:
        if task := await session.get(Task, task_id):
            task.update(payload)
            await session.commit()
            await session.refresh(task)
            return task
        return None
