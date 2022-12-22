from pydantic import BaseModel
from typing import List, Optional

class DeviceIn(BaseModel):
    name: str
    nationality: Optional[str] = None


class DeviceOut(DeviceIn):
    id: int


class DeviceUpdate(DeviceIn):
    name: Optional[str] = None