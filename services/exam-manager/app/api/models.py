# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definitions of pydantic models and helper functions."""

import uuid
from enum import Enum
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Extra, Field

from .db import Device, Exam, Job, Workflow


class XYZ(BaseModel):
    """XYZ model."""

    X: float
    Y: float
    Z: float


class SequenceParameters(BaseModel):
    """SequenceParameters model."""

    fov: XYZ
    fov_offset: XYZ


class Gender(str, Enum):
    """Gender model."""

    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    NOT_GIVEN = "NOT_GIVEN"


class AcquisitionLimits(BaseModel):
    """AcquisitionLimits models."""

    patient_height: float
    patient_weight: float
    patient_gender: Gender = Field(None, alias="Gender")
    patient_age: int


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


class TaskType(str, Enum):
    """Task type enum."""

    PROCESSING_TASK = "PROCESSING_TASK"
    DEVICE_TASK = "DEVICE_TASK"
    CERTIFIED_DEVICE_TASK = "CERTIFIED_DEVICE_TASK"
    CERTIFIED_PROCESSING_TASK = "CERTIFIED_PROCESSING_TASK"


class TaskStatus(str, Enum):
    """Task status enum."""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ERROR = "ERROR"

class BaseTask(BaseModel):
    """Task model."""

    job_id: uuid.UUID
    description: str
    type: TaskType
    args: dict[str, str]
    artifacts: dict[str, list[dict[str, str]]]
    task_destinations: list[dict[str, str]]
    status: dict[TaskStatus, str]


class TaskOut(BaseTask):
    """Task output model."""

    id: uuid.UUID
    datetime_created: datetime

class BaseJob(BaseModel):
    """Job base model."""

    class Config:
        """Base class configuration."""

        extra = Extra.ignore

    comment: str | None
    exam_id: uuid.UUID
    is_finished: bool


class JobOut(BaseJob):
    """Job output model."""

    id: uuid.UUID
    tasks: list[TaskOut]
    datetime_created: datetime
    datetime_updated: datetime | None


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


class ExamOut(BaseExam):
    """Exam output model."""

    id: uuid.UUID
    datetime_created: datetime
    datetime_updated: datetime | None
    jobs: list[JobOut]


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
    data.tasks = [await TaskOut(**task) for task in data.tasks]
    return JobOut(**data.__dict__)

    # return JobOut(
    #     id=data.id,
    #     type=data.type,
    #     comment=data.comment,
    #     is=data.is_acquired,
    #     exam_id=data.exam_id,
    #     sequence_id=data.sequence_id,
    #     device_id=data.device_id,
    #     workflow_id=data.workflow_id,
    #     device=await get_device_out(device) if device else None,
    #     workflow=await get_workflow_out(workflow) if workflow else None,
    #     tasks=tasks,
    #     datetime_created=data.datetime_created,
    #     datetime_updated=data.datetime_updated,
    #     acquisition_limits=data.acquisition_limits,
    #     sequence_parameters=data.sequence_parameters,
    # )


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
    # exam_jobs = [await get_job_out(job) for job in data.jobs]

    # return ExamOut(
    #     id=data.id,
    #     patient_id=data.patient_id,
    #     name=data.name,
    #     country=data.country,
    #     site=data.site,
    #     address=data.address,
    #     creator=data.creator,
    #     status=data.status,
    #     jobs=exam_jobs,
    #     datetime_created=data.datetime_created,
    #     datetime_updated=data.datetime_updated,
    # )
    exam = data.__dict__
    exam["jobs"] = [await get_job_out(job) for job in data.jobs]
    return ExamOut(**exam)

