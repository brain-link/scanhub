# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Data acess layer (DAL) between fastapi endpoint and sql database."""

from pprint import pprint
from uuid import UUID

from scanhub_libraries.models import BaseWorkflow
from sqlalchemy.engine import Result as SQLResult
from sqlalchemy.future import select

from app.db.postgres import Workflow, async_session


async def add_workflow_data(payload: BaseWorkflow, creator: str) -> Workflow:
    """Add new workflow.

    Parameters
    ----------
    payload
        Workflow pydantic base model with data for workflow creation
    creator
        The username/id of the user who creats this exam

    Returns
    -------
        Database orm model of created workflow
    """
    new_workflow = Workflow(**payload.dict(), creator=creator)
    async with async_session() as session:
        session.add(new_workflow)
        await session.commit()
        await session.refresh(new_workflow)
    # Debugging
    print("***** NEW WORKFLOW *****")
    pprint(new_workflow.__dict__)
    return new_workflow


async def get_workflow_data(workflow_id: UUID) -> (Workflow | None):
    """Get workflow by id.

    Parameters
    ----------
    workflow_id
        Id of the requested workflow

    Returns
    -------
        Database orm model with data of requested workflow
    """
    async with async_session() as session:
        workflow = await session.get(Workflow, workflow_id)
    return workflow


async def get_all_workflow_data(exam_id: UUID) -> list[Workflow]:
    """Get a list of all workflows assigned to a certain exam.

    Parameters
    ----------
    exam_id
        Id of the parent exam entry, workflows are assigned to

    Returns
    -------
        List of workflow data base orm models
    """
    async with async_session() as session:
        result: SQLResult = await session.execute(select(Workflow).where(Workflow.exam_id == exam_id))
        workflows = list(result.scalars().all())
    return workflows


async def get_all_workflows_template_data() -> list[Workflow]:
    """Get a list of all workflows assigned to a certain exam.

    Parameters
    ----------
    exam_id
        Id of the parent exam entry, workflows are assigned to

    Returns
    -------
        List of workflow data base orm models
    """
    async with async_session() as session:
        result: SQLResult = await session.execute(select(Workflow).where(Workflow.is_template))
        workflows = list(result.scalars().all())
    return workflows


async def delete_workflow_data(workflow_id: UUID) -> bool:
    """Delete a workflow by ID. Cascade delete the associated tasks.

    Parameters
    ----------
    workflow_id
        ID of workflow to be deleted

    Returns
    -------
        Success of delete event
    """
    async with async_session() as session:
        if workflow := await session.get(Workflow, workflow_id):
            for task in workflow.tasks:
                await session.delete(task)
            await session.delete(workflow)
            await session.commit()
            return True
        return False


async def update_workflow_data(workflow_id: UUID, payload: BaseWorkflow) -> (Workflow | None):
    """Update existing workflow in database.

    Parameters
    ----------
    workflow_id
        Id of the workflow to be updateed
    payload
        Workflow pydantic base model with data to be updated

    Returns
    -------
        Workflow database orm model of updated workflow
    """
    async with async_session() as session:
        if workflow := await session.get(Workflow, workflow_id):
            workflow.update(payload)
            await session.commit()
            await session.refresh(workflow)
            return workflow
        return None
