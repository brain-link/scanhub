from pydantic import BaseModel
from typing import List, Optional

class RecoIn(BaseModel):
    name: str
    plot: str
    genres: List[str]
    devices_id: List[int]


class RecoOut(RecoIn):
    id: int


class RecoUpdate(RecoIn):
    name: Optional[str] = None
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    devices_id: Optional[List[int]] = None