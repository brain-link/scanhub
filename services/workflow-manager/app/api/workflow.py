"""Workflow manager endpoints."""
import json

from api import dal
from api.models import BaseWorkflow, WorkflowOut, get_workflow_out
from fastapi import APIRouter, HTTPException
from kafka import KafkaProducer

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found

producer = KafkaProducer(
    bootstrap_servers=['kafka-broker:9093'],
    value_serializer=lambda x: json.dumps(x.__dict__).encode('utf-8')
)

router = APIRouter()


@router.post('/', response_model=WorkflowOut, status_code=201, tags=["workflow"])
async def create_workflow(payload: BaseWorkflow) -> WorkflowOut:
    """Create new workflow endpoint.

    Parameters
    ----------
    payload
        Workflow pydantic base model

    Returns
    -------
        Workflow pydantic output model

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    workflow = await dal.add_workflow(payload)
    if not workflow:
        raise HTTPException(status_code=404, detail="Could not create workflow")
    return await get_workflow_out(workflow)


@router.get('/{workflow_id}', response_model=WorkflowOut, status_code=200, tags=["workflow"])
async def get_workflow(workflow_id: int) -> WorkflowOut:
    """Get workflow endpoint.

    Parameters
    ----------
    workflow_id
        Id of the workflow object to be returned

    Returns
    -------
        Workflow pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    workflow = await dal.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return await get_workflow_out(workflow)


@router.get('/', response_model=list[WorkflowOut], status_code=200, tags=["workflow"])
async def get_workflow_list() -> list[WorkflowOut]:
    """Get all workflows endpoint.

    Returns
    -------
        List of workflow pydantic output models, might be empty
    """
    workflows = await dal.get_all_workflows()
    if not workflows:
        # raise HTTPException(status_code=404, detail="Workflows not found")
        return []
    else:
        return [await get_workflow_out(workflow) for workflow in workflows]


@router.delete('/{workflow_id}', response_model={}, status_code=204, tags=["workflow"])
async def delete_workflow(workflow_id: int) -> None:
    """Delete workflow endpoint.

    Parameters
    ----------
    workflow_id
        Id of workflow to be deleted

    Raises
    ------
    HTTPException
        404: Not found
    """
    if not await dal.delete_workflow(workflow_id):
        raise HTTPException(status_code=404, detail="Workflow not found")


@router.put('/{workflow_id}/', response_model=WorkflowOut, status_code=200, tags=["workflow"])
async def update_workflow(workflow_id: int, payload: BaseWorkflow) -> WorkflowOut:
    """Update existing workflow endpoint.

    Parameters
    ----------
    workflow_id
        Id of the workflow to be updated
    payload
        Data to be updated, workflow pydantic base model

    Returns
    -------
        Workflow pydantic output model.

    Raises
    ------
    HTTPException
        404: Not found
    """
    workflow = await dal.update_workflow(workflow_id, payload)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return await get_workflow_out(workflow)
