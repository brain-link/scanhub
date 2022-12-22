from app.api.models import WorkflowIn, WorkflowOut, WorkflowUpdate
from app.api.db import workflow, database


async def add_workflow(payload: WorkflowIn):
    query = workflow.insert().values(**payload.dict())

    return await database.execute(query=query)

async def get_workflow(id):
    query = workflow.select(workflow.c.id==id)
    return await database.fetch_one(query=query)