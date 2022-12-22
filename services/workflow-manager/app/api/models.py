from pydantic import BaseModel
from typing import List, Optional

class WorkflowIn(BaseModel):
    name: str
    nationality: Optional[str] = None


class WorkflowOut(WorkflowIn):
    id: int


class WorkflowUpdate(WorkflowIn):
    name: Optional[str] = None