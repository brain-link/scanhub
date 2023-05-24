"""Workflow data access layer."""

from pprint import pprint
from typing import Sequence

from api.db import Workflow, async_session
from api.models import BaseWorkflow
from sqlalchemy.future import select


async def add_workflow(payload: BaseWorkflow) -> Workflow:
    """Add a new workflow to the database.

    Arguments:
        payload {BaseWorkflow} -- Pydantic base model to create a new database entry

    Returns:
        Workflow -- Database orm model
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


async def get_workflow(id: int) -> Workflow:
    """Fetch a workflow from database.

    Arguments:
        id {int} -- ID of workflow

    Returns:
        Workflow -- Database orm model
    """
    async with async_session() as session:
        workflow = await session.get(Workflow, id)
    return workflow


async def get_all_workflows() -> Sequence[Workflow]:
    """Get a list of all existing workflows.

    Returns:
        List[Workflow] -- List of database orm models
    """
    async with async_session() as session:
        result = await session.execute(select(Workflow))
        workflows = result.scalars().all()
    return workflows


async def delete_workflow(id: int) -> bool:
    """Delete a workflow by ID.

    Arguments:
        id {int} -- ID of workflow to be deleted

    Returns:
        bool -- Success of delete event
    """
    async with async_session() as session:
        workflow = await session.get(Workflow, id)
        if workflow:
            await session.delete(workflow)
            await session.commit()
            return True
        else:
            return False
        # TODO: What to return here?


async def update_workflow(id: int, payload: BaseWorkflow) -> Workflow | None:
    """Update an existing workflow in database.

    Arguments:
        id {int} -- ID of workflow
        payload {BaseWorkflow} -- Pydantic base model, data to be updated

    Returns:
        Workflow -- Updated database orm model
    """
    async with async_session() as session:
        workflow = await session.get(Workflow, id)
        if workflow:
            workflow.update(payload.dict())
            await session.commit()
            await session.refresh(workflow)
            return workflow
        else:
            return None
