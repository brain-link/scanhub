"""Workflow data access layer."""

from pprint import pprint

from api.db import Workflow, async_session
from api.models import BaseWorkflow
from sqlalchemy.engine import Result
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
    """Get a list of all existing workflows.

    Returns:
        List[Workflow] -- List of database orm models
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
        if (workflow := await session.get(Workflow, workflow_id)):
            await session.delete(workflow)
            await session.commit()
            return True
        return False


async def update_workflow(workflow_id: int, payload: BaseWorkflow) -> (Workflow | None):
    """Update an existing workflow in database.

    Arguments:
        workflow_id {int} -- ID of workflow
        payload {BaseWorkflow} -- Pydantic base model, data to be updated

    Returns:
        Workflow -- Updated database orm model
    """
    async with async_session() as session:
        if (workflow := await session.get(Workflow, workflow_id)):
            workflow.update(payload.dict())
            await session.commit()
            await session.refresh(workflow)
            return workflow
        return None
