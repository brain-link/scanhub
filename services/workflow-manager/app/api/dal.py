# data access layer (DAL)

from sqlalchemy.future import select
from sqlalchemy import update
from pprint import pprint
from typing import List

from api.models import BaseWorkflow, WorkflowOut, get_workflow_out
from api.db import Workflow, async_session



async def add_workflow(payload: BaseWorkflow) -> WorkflowOut:
    new_workflow = Workflow(**payload.dict())
    async with async_session() as session:
        session.add(new_workflow)
        await session.commit()
        await session.refresh(new_workflow)
    print("***** NEW WORKFLOW *****")
    pprint(new_workflow.__dict__)
    return await get_workflow_out(new_workflow)


async def get_workflow(id: int) -> WorkflowOut:
    async with async_session() as session:
        workflow = await session.get(Workflow, id)
    return await get_workflow_out(workflow)


async def get_all_workflows() -> List[WorkflowOut]:
    async with async_session() as session:
        result = await session.execute(select(Workflow))
        workflows = result.scalars().all()
    return [await get_workflow_out(workflow) for workflow in workflows]


async def delete_workflow(id: int) -> bool:
    async with async_session() as session:
        workflow = await session.get(Workflow, id)
        if workflow:
            await session.delete(workflow)
            await session.commit()
            return True
        else: 
            return False
        # TODO: What to return here?


async def update_workflow(id: int, payload: BaseWorkflow) -> WorkflowOut:
    async with async_session() as session:
        workflow = await session.get(Workflow, id)
        workflow.update(payload.dict())
        await session.commit()
        await session.refresh(workflow)
        
    return await get_workflow_out(workflow)