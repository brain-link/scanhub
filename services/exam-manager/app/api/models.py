from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from api.db import Exam, Procedure, Record, Device, Workflow

# TODO: Define model id's as uuid's


#***********************************************
#   Base Models
#***********************************************

class BaseDevice(BaseModel):
    name: str
    manufacturer: str
    modality: str
    status: str
    site: Optional[str] = None
    ip_address: str

class BaseWorkflow(BaseModel):
    host: str
    name: str
    manufacturer: str
    modality: str
    type: str
    status: str
    kafka_topic: str

class BaseExam(BaseModel):
    patient_id: int
    name: str
    country: Optional[str] = None
    site: Optional[str] = None
    address: Optional[str] = None
    creator: str
    status: str

class BaseProcedure(BaseModel):
    name: str
    modality: str
    status: str

class BaseRecord(BaseModel):
    status: str
    comment: Optional[str] = None


#***********************************************
#   Insert Models
#***********************************************

class ProcedureIn(BaseProcedure):
    exam_id: int

class RecordIn(BaseRecord):
    sequence_id: int
    workflow_id: Optional[int] = None
    device_id: int
    procedure_id: int


#***********************************************
#   Output Models
#***********************************************

class DeviceOut(BaseDevice):
    id: int
    datetime_created: datetime
    datetime_updated: datetime | None

class WorkflowOut(BaseWorkflow):
    id: int
    datetime_created: datetime
    datetime_updated: datetime | None

class RecordOut(BaseRecord):
    id: int
    is_acquired: bool
    datetime_created: datetime
    datetime_updated: datetime | None
    device: Optional[DeviceOut] = None
    workflow: Optional[WorkflowOut] = None
    # TODO: return sequence object

class ProcedureOut(BaseProcedure):
    id: int
    datetime_created: datetime
    datetime_updated: datetime | None
    records: List[RecordOut]

class ExamOut(BaseExam):
    id: int
    datetime_created: datetime
    datetime_updated: datetime | None
    procedures: List[ProcedureOut]



#***********************************************
#   Helper: SQLAlchemy-ORM to Pydantic
#***********************************************

async def get_workflow_out(data: Workflow) -> WorkflowOut:
    return WorkflowOut(
        id=data.id,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
        host=data.host,
        name=data.name,
        manufacturer=data.manufacturer,
        modality=data.modality,
        type=data.type,
        status=data.status,
        kafka_topic=data.kafka_topic,
    )

async def get_device_out(data: Device) -> DeviceOut:
    return DeviceOut(
        id=data.id,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
        name=data.name,
        manufacturer=data.manufacturer,
        modality=data.modality,
        status=data.status,
        site=data.site,
        ip_address=data.ip_address,
    )

async def get_record_out(data: Record, device: Device = None, workflow: Workflow = None) -> RecordOut:
    return RecordOut(
        id=data.id,
        status=data.status,
        comment=data.comment,
        is_acquired=data.is_acquired,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
        # TODO: How/where to fetch device and workflow? 
        device=await get_device_out(device) if device else None,
        workflow=await get_workflow_out(workflow) if workflow else None,
        # sequence=...
    )

async def get_procedure_out(data: Procedure) -> ProcedureOut:

    # Create records of the procedure
    records = [await get_record_out(record) for record in data.records]

    return ProcedureOut(
        id=data.id,
        name=data.name,
        status=data.status,
        modality=data.modality,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
        records=records
    )

async def get_exam_out(data: Exam) -> ExamOut:

    # Create procedures of the exam
    exam_procedures = [await get_procedure_out(procedure) for procedure in data.procedures]

    return ExamOut(
        id=data.id,
        patient_id=data.patient_id,
        name=data.name,
        country=data.country,
        site=data.site,
        address=data.address,
        creator=data.creator,
        status=data.status,
        procedures=exam_procedures,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
    )
