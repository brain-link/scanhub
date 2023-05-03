from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from api.db import Workflow


class BaseWorkflow(BaseModel):
    host: str
    name: str
    author: Optional[str] = None
    modality: str
    type: str
    status: str
    kafka_topic: str


class WorkflowOut(BaseWorkflow):
    id: int # uuid
    datetime_created: datetime
    datetime_updated: datetime | None


async def get_workflow_out(data: Workflow) -> WorkflowOut:
    return WorkflowOut(
        id=data.id,
        host=data.host,
        name=data.name,
        author=data.author,
        modality=data.modality,
        type=data.type,
        status=data.status,
        kafka_topic=data.kafka_topic,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
    )