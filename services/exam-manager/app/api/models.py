from pydantic import BaseModel
from typing import List, Optional
from api.db import Exam, Procedure  #, Record, Device, Workflow
from datetime import datetime
import uuid
import pprint

# TODO: Definition of models in scanhub-tools, otherwise redundant model definition

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
    patient_id: str
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
    sequence_id: int


#***********************************************
#   Insert Models
#***********************************************

class ProcedureIn(BaseProcedure):
    exam_id: int

class RecordIn(BaseRecord):
    procedure_id: int
    workflow_id: Optional[int] = None
    device_id: int



#***********************************************
#   Output Models
#***********************************************

class DeviceOut(BaseDevice):
    id: str
    datetime_created: datetime
    datetime_updated: datetime | None

class WorkflowOut(BaseWorkflow):
    id: str
    datetime_created: datetime
    datetime_updated: datetime | None

class RecordOut(BaseRecord):
    id: str
    is_acquired: bool
    datetime_created: datetime
    datetime_updated: datetime | None
    device: DeviceOut
    workflow: WorkflowOut

class ProcedureOut(BaseProcedure):
    id: str
    datetime_created: datetime
    datetime_updated: datetime | None
    records: List[RecordOut]

class ExamOut(BaseExam):
    id: str
    datetime_created: datetime
    datetime_updated: datetime | None
    procedures: List[ProcedureOut]

#***********************************************
#   Transformer: SQLAlchemy-ORM to Pydantic
#***********************************************

# async def get_workflow_out(data: Workflow) -> WorkflowOut:
#     return WorkflowOut(
#         id=str(data.id),
#         datetime_created=data.datetime_created,
#         datetime_updated=data.datetime_updated,
#         host=data.host,
#         name=data.name,
#         manufacturer=data.manufacturer,
#         modality=data.modality,
#         type=data.type,
#         status=data.status,
#         kafka_topic=data.kafka_topic,
#     )

# async def get_device_out(data: Device) -> DeviceOut:
#     return DeviceOut(
#         id=str(data.id),
#         datetime_created=data.datetime_created,
#         datetime_updated=data.datetime_updated,
#         name=data.name,
#         manufacturer=data.manufacturer,
#         modality=data.modality,
#         status=data.status,
#         site=data.site,
#         ip_address=data.ip_address,
#     )

# async def get_record_out(data: Exam) -> RecordOut:

#     return RecordOut(
#         id=str(data.id),
#         sequence_id=data.sequence_id,
#         is_acquired=data.is_acquired,
#         datetime_created=data.datetime_created,
#         datetime_updated=data.datetime_updated,
#         device=get_device_out(data.device),
#         workflow=get_workflow_out(data.workflow) if hasattr(data, "workflow") else None,
#     )

async def get_procedure_out(data: Procedure) -> ProcedureOut:
    # records = [get_record_out(record) for record in data.records] if hasattr(data, "records") else []
    records = []
    return ProcedureOut(
        id=str(data.id),
        name=data.name,
        status=data.status,
        modality=data.modality,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
        records=records
    )

async def get_exam_out(data: Exam) -> ExamOut:

    # exam_procedures = []
    # for procedure in data.procedures:
    #     procedure_out = await get_procedure_out(procedure)
    #     exam_procedures.append(procedure_out)

    exam_procedures = [
        await get_procedure_out(procedure) for procedure in data.procedures
    ]
    
    return ExamOut(
        id=str(data.id),
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
