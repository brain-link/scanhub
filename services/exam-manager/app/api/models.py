from pydantic import BaseModel
from typing import List, Optional

class ExamIn(BaseModel):
    name: str
    nationality: Optional[str] = None


class ExamOut(ExamIn):
    id: int


class ExamUpdate(ExamIn):
    name: Optional[str] = None