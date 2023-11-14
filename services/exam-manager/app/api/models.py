# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definitions of pydantic models and helper functions."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Extra

from .db import AcquisitionLimits, Device, Exam, Job, Procedure, Record, SequenceParameters, Workflow


class Commands(str, Enum):
    """Commands model."""

    START = "START"
    STOP = "STOP"
    PAUSE = "PAUSE"


class BaseDevice(BaseModel):
    """Device base model."""

    class Config:
        """Base class configuration."""

        extra = Extra.ignore

    name: str
    manufacturer: str
    modality: str
    status: str
    site: str | None
    ip_address: str


class BaseWorkflow(BaseModel):
    """Workflow base model."""

    class Config:
        """Base class configuration."""

        extra = Extra.ignore

    host: str
    name: str
    manufacturer: str
    modality: str
    type: str
    status: str
    kafka_topic: str


class BaseExam(BaseModel):
    """Exam base model."""

    class Config:
        """Base class configuration."""

        extra = Extra.ignore

    patient_id: int
    name: str
    country: str | None
    site: str | None
    address: str | None
    creator: str
    status: str


class BaseProcedure(BaseModel):
    """Procedure base model."""

    class Config:
        """Base class configuration."""

        extra = Extra.ignore

    name: str
    status: str


class BaseJob(BaseModel):
    """Job base model."""

    class Config:
        """Base class configuration."""

        extra = Extra.ignore

    type: str
    comment: str | None
    procedure_id: int
    sequence_id: str
    workflow_id: int | None
    device_id: str
    acquisition_limits: AcquisitionLimits
    sequence_parameters: SequenceParameters


class BaseRecord(BaseModel):
    """Record base model."""

    class Config:
        """Base class configuration."""

        extra = Extra.ignore

    data_path: str | None
    comment: str | None


class ProcedureIn(BaseProcedure):
    """Procedure input model."""

    exam_id: int


class RecordIn(BaseRecord):
    """Record input model."""

    job_id: int


class DeviceOut(BaseDevice):
    """Devicee output model."""

    id: str
    datetime_created: datetime
    datetime_updated: datetime | None


class WorkflowOut(BaseWorkflow):
    """Workflow output model."""

    id: int
    datetime_created: datetime
    datetime_updated: datetime | None


class RecordOut(BaseRecord):
    """Record output model."""

    id: int
    datetime_created: datetime


class JobOut(BaseJob):
    """Job output model."""

    id: int
    is_acquired: bool
    device: DeviceOut | None
    workflow: WorkflowOut | None
    records: list[RecordOut]
    datetime_created: datetime
    datetime_updated: datetime | None


class ProcedureOut(BaseProcedure):
    """Procedure output model."""

    id: int
    datetime_created: datetime
    datetime_updated: datetime | None
    jobs: list[JobOut]


class ExamOut(BaseExam):
    """Exam output model."""

    id: int
    datetime_created: datetime
    datetime_updated: datetime | None
    procedures: list[ProcedureOut]


async def get_workflow_out(data: Workflow) -> WorkflowOut:
    """Workflow output helper function.

    Parameters
    ----------
    data
        Workflow database model

    Returns
    -------
        Workflow pydantic output model
    """
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
    """Device output helper function.

    Parameters
    ----------
    data
        Device database model

    Returns
    -------
        Device pydantic output model
    """
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
    """Record output helper function.

    Parameters
    ----------
    data
        Record database model

    Returns
    -------
        Record pydantic output model
    """
    return RecordOut(
        id=data.id,
        data_path=data.data_path,
        comment=data.comment,
        datetime_created=data.datetime_created,
    )


async def get_job_out(data: Job, device: Device = None, workflow: Workflow = None) -> JobOut:
    """Job output helper function.

    Parameters
    ----------
    data
        Job database model
    device, optional
        Device database model, by default None
    workflow, optional
        Workflow database model, by default None

    Returns
    -------
        Job pydantic output model
    """
    # Create records of the job
    records = [await get_record_out(record) for record in data.records]

    return JobOut(
        id=data.id,
        type=data.type,
        comment=data.comment,
        is_acquired=data.is_acquired,
        procedure_id=data.procedure_id,
        sequence_id=data.sequence_id,
        device_id=data.device_id,
        workflow_id=data.workflow_id,
        device=await get_device_out(device) if device else None,
        workflow=await get_workflow_out(workflow) if workflow else None,
        records=records,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
        acquisition_limits=data.acquisition_limits,
        sequence_parameters=data.sequence_parameters,
    )


async def get_procedure_out(data: Procedure) -> ProcedureOut:
    """Procedure output helper function.

    Parameters
    ----------
    data
        Procedure database model

    Returns
    -------
        Procedure pydantic output model
    """
    # Create jobs of the procedure
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
    """Exam output helper function.

    Parameters
    ----------
    data
        Exam database model

    Returns
    -------
        Exam pydantic output model
    """
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
