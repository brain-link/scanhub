# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow data access layer."""

from pprint import pprint

from sqlalchemy.engine import Result
from sqlalchemy.future import select

from .db import Workflow, async_session
from .models import BaseWorkflow, WorkflowIn


async def add_workflow(payload: WorkflowIn) -> Workflow:
    """Add new workflow to database.

    Parameters
    ----------
    payload
        Workflow pydantic base model with data of new workflow entry

    Returns
    -------
        Database orm model of new workflow
    """
    new_workflow = Workflow(**payload.dict())
    async with async_session() as session:
        session.add(new_workflow)
        await session.commit()
        await session.refresh(new_workflow)
    # Debugging
    print("***** NEW WORKFLOW *****")
    pprint(new_workflow.__dict__)
    return new_workflow


async def get_workflow(workflow_id: int) -> (Workflow | None):
    """Get workflow from database.

    Parameters
    ----------
    workflow_id
        Id of workflow to be returned

    Returns
    -------
        Workflow database ORM model if exists
    """
    async with async_session() as session:
        workflow = await session.get(Workflow, workflow_id)
    return workflow


async def get_all_workflows() -> list[Workflow]:
    """Get a list of all workflows.

    Returns
    -------
        List of workflow database orm models
    """
    async with async_session() as session:
        result: Result = await session.execute(select(Workflow))
        workflows = list(result.scalars().all())
    return workflows


async def delete_workflow(workflow_id: int) -> bool:
    """Delete workflow entry by id.

    Parameters
    ----------
    workflow_id
        Id of the workflow to be deleted

    Returns
    -------
        Success of delete eveent
    """
    async with async_session() as session:
        if workflow := await session.get(Workflow, workflow_id):
            await session.delete(workflow)
            await session.commit()
            return True
        return False


async def update_workflow(workflow_id: int, payload: BaseWorkflow) -> (Workflow | None):
    """Update existing workflow in database by id.

    Parameters
    ----------
    workflow_id
        Id of the workflow to be updated

    payload
        Workflow pydantic base model with data  to be updated

    Returns
    -------
        Updated workflow database orm model, if update successful
    """
    async with async_session() as session:
        if workflow := await session.get(Workflow, workflow_id):
            workflow.update(payload)
            await session.commit()
            await session.refresh(workflow)
            return workflow
        return None
