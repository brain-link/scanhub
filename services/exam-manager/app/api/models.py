from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Extra

from api.db import Exam, Procedure, Job, Record, Device, Workflow

# TODO: Define model id's as uuid's


# ***********************************************
# Base Models
# ***********************************************

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

    class Config:
        extra = Extra.ignore

    patient_id: int
    name: str
    country: Optional[str] = None
    site: Optional[str] = None
    address: Optional[str] = None
    creator: str
    status: str


class BaseProcedure(BaseModel):

    class Config:
        extra = Extra.ignore

    name: str
    status: str


class BaseJob(BaseModel):

    class Config:
        extra = Extra.ignore

    type: str
    comment: Optional[str] = None
    sequence_id: str
    workflow_id: Optional[int] = None
    device_id: int


class BaseRecord(BaseModel):

    class Config:
        extra = Extra.ignore

    data_path: Optional[str] = None
    comment: Optional[str] = None


# ***********************************************
# Insert Models
# ***********************************************

class ProcedureIn(BaseProcedure):
    exam_id: int


class RecordIn(BaseRecord):
    job_id: int


class JobIn(BaseJob):
    procedure_id: int


# ***********************************************
# Output Models
# ***********************************************

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
    datetime_created: datetime


class JobOut(BaseJob):
    id: int
    is_acquired: bool
    device: Optional[DeviceOut] = None
    workflow: Optional[WorkflowOut] = None
    records: List[RecordOut]
    datetime_created: datetime
    datetime_updated: Optional[datetime] = None


class ProcedureOut(BaseProcedure):
    id: int
    datetime_created: datetime
    datetime_updated: datetime | None
    jobs: List[JobOut]


class ExamOut(BaseExam):
    id: int
    datetime_created: datetime
    datetime_updated: datetime | None
    procedures: List[ProcedureOut]


# ***********************************************
# Helper: SQLAlchemy-ORM to Pydantic
# ***********************************************

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


async def get_record_out(data: Record) -> RecordOut:
    return RecordOut(
        id=data.id,
        job_id=data.job_id,
        data_path=data.data_path,
        comment=data.comment,
        datetime_created=data.datetime_created
    )


async def get_job_out(data: Job, device: Device = None, workflow: Workflow = None) -> JobOut:

    records = [await get_record_out(record) for record in data.records]

    return JobOut(
        id=data.id,
        type=data.type,
        comment=data.comment,
        is_acquired=data.is_acquired,
        sequence_id=data.sequence_id,
        device_id=data.device_id,
        workflow_id=data.workflow_id,
        device=await get_device_out(device) if device else None,
        workflow=await get_workflow_out(workflow) if workflow else None,
        records=records,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
    )


async def get_procedure_out(data: Procedure) -> ProcedureOut:

    # Create records of the procedure
    # records = [await get_record_out(record) for record in data.records]
    jobs = [await get_job_out(job) for job in data.jobs]

    return ProcedureOut(
        id=data.id,
        name=data.name,
        status=data.status,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
        jobs=jobs,
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
