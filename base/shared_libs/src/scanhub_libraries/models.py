# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Pydantic models of acquisition control."""
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Extra, Field, Json  # noqa


class Gender(str, Enum):
    """Pydantic definition of genders."""

    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    NOT_GIVEN = "NOT_GIVEN"


class Commands(str, Enum):
    """Pydantic definition of a commands."""

    START = "START"
    STOP = "STOP"
    PAUSE = "PAUSE"


class XYZ(BaseModel):
    """Pydantic definition of coordinates."""

    X: float
    Y: float
    Z: float


class AcquisitionLimits(BaseModel):
    """Pydantic definition of AcquisitionLimits."""

    patient_height: float
    patient_weight: float
    patient_gender: Gender = Field(None, alias="Gender")
    patient_age: int


class SequenceParameters(BaseModel):
    """Pydantic definition of SequenceParameters."""

    fov: XYZ
    fov_offset: XYZ


class ScanJob(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic model definition of a scanjob."""

    class Config:
        """Pydantic configuration."""

        extra = Extra.ignore

    job_id: UUID = Field(alias="id")
    sequence_id: str
    workflow_id: int
    device_id: str
    acquisition_limits: AcquisitionLimits
    sequence_parameters: SequenceParameters


class ParametrizedSequence(BaseModel):
    """Pydantic model definition of a parametrized sequence."""

    acquisition_limits: AcquisitionLimits
    sequence_parameters: SequenceParameters
    sequence: Json


class MRISequence(BaseModel):
    """A class representing an MRI sequence definition file and its associated metadata.

    Attributes
    ----------
        id: The unique identifier for the MRI sequence, autogenerated by MongoDB.
        name: The name of the MRI sequence.
        description: A brief description of the MRI sequence.
        sequence_type: The type of MRI sequence, such as T1-weighted, T2-weighted, etc.
        created_at: The timestamp of when the MRI sequence was created.
        updated_at: The timestamp of when the MRI sequence was last updated.
        tags: A list of tags or keywords associated with the MRI sequence, useful for searching and filtering.
        file: The MRI sequence definition file content or a reference to the stored file,
        such as a GridFS identifier or an S3 URL.
        file_extension: The file extension of the MRI sequence definition file.
    """

    id: str | None = Field(alias="_id")
    name: str
    description: str | None
    sequence_type: str | None
    created_at: datetime | None
    updated_at: datetime | None
    tags: list[str] | None
    file: Any
    file_extension: str | None


class MRISequenceCreate(BaseModel):
    """A class representing an MRI sequence definition file and its associated metadata.

    Attributes
    ----------
        id: The unique identifier for the MRI sequence, autogenerated by MongoDB.
        name: The name of the MRI sequence.
        description: A brief description of the MRI sequence.
        sequence_type: The type of MRI sequence, such as T1-weighted, T2-weighted, etc.
        created_at: The timestamp of when the MRI sequence was created.
        updated_at: The timestamp of when the MRI sequence was last updated.
        tags: A list of tags or keywords associated with the MRI sequence, useful for searching and filtering.
    """

    id: str | None = Field(alias="_id", default=None)
    name: str
    description: str | None = None
    sequence_type: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    tags: list[str] | None = None


class DeviceTask(BaseModel):
    """Pydantic model definition of a device job."""

    device_id: str
    record_id: UUID
    command: Commands
    parametrized_sequence: ParametrizedSequence


class ScanStatus(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of a scanjob."""

    record_id: UUID
    status_percent: int


class ScanRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of data to receive."""

    record_id: UUID


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

    patient_id: UUID
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

    exam_id: UUID | str


class RecordIn(BaseRecord):
    """Record input model."""

    job_id: UUID


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

    id: UUID
    datetime_created: datetime


class JobOut(BaseJob):
    """Job output model."""

    id: UUID
    is_acquired: bool
    device: DeviceOut | None
    workflow: WorkflowOut | None
    records: list[RecordOut]
    datetime_created: datetime
    datetime_updated: datetime | None


class ExamOut(BaseExam):
    """Exam output model."""

    id: UUID
    datetime_created: datetime
    datetime_updated: datetime | None
    jobs: list[JobOut]
