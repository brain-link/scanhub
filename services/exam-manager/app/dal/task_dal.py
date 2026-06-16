# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Data access layer (DAL) between fastapi endpoint and sql database."""

from uuid import UUID

from scanhub_libraries.models import BaseAcquisitionTask
from sqlalchemy import func
from sqlalchemy.future import select

from app.db.postgres import AcquisitionTask, Task, async_session


async def add_task_data(payload: BaseAcquisitionTask, creator: str) -> AcquisitionTask:
    """Add new acquisition task to database."""
    new_task = AcquisitionTask(**payload.model_dump(), creator=creator)

    async with async_session() as session:
        if new_task.workflow_id:
            result = await session.execute(
                select(func.max(Task.position)).where(Task.workflow_id == new_task.workflow_id)
            )
            max_position = result.scalar()
            new_task.position = (max_position + 1) if max_position is not None else 0

        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
    return new_task


async def get_task_data(task_id: UUID) -> AcquisitionTask | None:
    """Get acquisition task by id."""
    async with async_session() as session:
        result = await session.execute(select(AcquisitionTask).where(AcquisitionTask.id == task_id))
        return result.scalar_one_or_none()


async def get_all_task_data(workflow_id: UUID) -> list[AcquisitionTask]:
    """Get all acquisition tasks assigned to a workflow, ordered by position."""
    async with async_session() as session:
        result = await session.execute(
            select(AcquisitionTask).where(AcquisitionTask.workflow_id == workflow_id).order_by(AcquisitionTask.position)
        )
        return list(result.scalars().all())


async def get_all_task_template_data() -> list[AcquisitionTask]:
    """Get all acquisition task templates."""
    async with async_session() as session:
        result = await session.execute(
            select(AcquisitionTask).where(AcquisitionTask.is_template).order_by(AcquisitionTask.position)
        )
        return list(result.scalars().all())


async def delete_task_data(task_id: UUID) -> bool:
    """Delete acquisition task by id."""
    async with async_session() as session:
        result = await session.execute(select(AcquisitionTask).where(AcquisitionTask.id == task_id))
        if task := result.scalar_one_or_none():
            await session.delete(task)
            await session.commit()
            return True
        return False


async def update_task_data(task_id: UUID, payload: BaseAcquisitionTask) -> AcquisitionTask | None:
    """Update existing acquisition task in database."""
    async with async_session() as session:
        result = await session.execute(select(AcquisitionTask).where(AcquisitionTask.id == task_id))
        if task := result.scalar_one_or_none():
            task.update(payload)
            await session.commit()
            await session.refresh(task)
            return task
        return None


async def update_task_status(task_id: UUID, status: str) -> AcquisitionTask | None:
    """Update only the status field of an acquisition task."""
    async with async_session() as session:
        result = await session.execute(select(AcquisitionTask).where(AcquisitionTask.id == task_id))
        if task := result.scalar_one_or_none():
            task.status = status
            await session.commit()
            await session.refresh(task)
            return task
        return None


async def reorder_tasks_data(task_ids: list[UUID]) -> bool:
    """Update the position of multiple tasks."""
    async with async_session() as session:
        for index, task_id in enumerate(task_ids):
            result = await session.execute(select(AcquisitionTask).where(AcquisitionTask.id == task_id))
            if task := result.scalar_one_or_none():
                task.position = index
        await session.commit()
        return True
