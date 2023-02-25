from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class RecordIDList(BaseModel):
    procedure_id: str
    id_list: List[str]

class Device(BaseModel):
    id: str

class Sequence(BaseModel):
    id: str
    parameters: Dict[str, Any]

class Processing(BaseModel):
    id: str
    parameters: Dict[str, Any]

class Record(BaseModel):
    id: str
    sequence: Sequence
    device: Device
    processing: Processing

class Procedure(BaseModel):
    id: str
    records: List[Record]

class Status(BaseModel):
    id: str
    status: str
