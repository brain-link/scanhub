# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Data acess layer (DAL) between fastapi endpoint and sql database."""

from uuid import UUID

from scanhub_libraries.models import BaseResult
from sqlalchemy.engine import Result as SQLResult
from sqlalchemy.future import select

from app.db import Result, async_session


async def add_result_db(payload: BaseResult) -> Result:
    """Add new result to database.

    Parameters
    ----------
    payload
        Result pydantic base model

    Returns
    -------
        Database orm model of created result
    """
    new_result = Result(**payload.dict())
    async with async_session() as session:
        session.add(new_result)
        await session.commit()
        await session.refresh(new_result)
    return new_result


async def get_result_db(resuld_id: UUID) -> Result | None:
    """Get result by id.

    Parameters
    ----------
    result_id
        Id of the requested result

    Returns
    -------
        Database orm model with data of requested result
    """
    async with async_session() as session:
        return await session.get(Result, resuld_id)

async def get_all_results_db(task_id: UUID) -> list[Result]:
    """Get a list of all results assigned to a certain task.

    Parameters
    ----------
    task_id
        Id of the parent task entry, results are assigned to

    Returns
    -------
        List of result data base orm models
    """
    async with async_session() as session:
        result: SQLResult = await session.execute(select(Result).where(Result.task_id == task_id))
        return list(result.scalars().all())

async def update_result_db(result_id: UUID, payload: BaseResult) -> Result | None:
    """Update existing result in database.

    Parameters
    ----------
    result_id
        Id of the result to be updateed
    payload
        Result pydantic base model with data to be updated

    Returns
    -------
        Resuld database orm model of updated result
    """
    async with async_session() as session:
        if result := await session.get(Result, result_id):
            result.update(payload)
            await session.commit()
            await session.refresh(result)
            return result
    return None

async def delete_result_db(result_id: UUID) -> bool:
    """Delete result by id.

    Parameters
    ----------
    result_id
        Id of the result to be deleted

    Returns
    -------
        Success of deletion
    """
    async with async_session() as session:
        if result := await session.get(Result, result_id):
            await session.delete(result)
            await session.commit()
            return True
    return False
