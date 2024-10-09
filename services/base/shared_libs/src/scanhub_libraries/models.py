# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Pydantic models of acquisition control."""
from datetime import date, datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID
from typing import Literal

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


# TODO: Move these parameters to the patient model.
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


# Might be obsolete
class ScanWorkflow(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic model definition of a scan workflow."""

    class Config:
        """Pydantic configuration."""

        extra = Extra.ignore

    workflow_id: UUID = Field(alias="id")
    sequence_id: str
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
        id:     The unique identifier for the MRI sequence, autogenerated by MongoDB.
        name:   The name of the MRI sequence.
        description:    A brief description of the MRI sequence.
        sequence_type:  The type of MRI sequence, such as T1-weighted, T2-weighted, etc.
        created_at:     The timestamp of when the MRI sequence was created.
        updated_at:     The timestamp of when the MRI sequence was last updated.
        tags:   A list of tags or keywords associated with the MRI sequence, useful for
                searching and filtering.
        file:   The MRI sequence definition file content or a reference to the stored 
                file, such as a GridFS identifier or an S3 URL.
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
        id:     The unique identifier for the MRI sequence, autogenerated by MongoDB.
        name:   The name of the MRI sequence.
        description:    A brief description of the MRI sequence.
        sequence_type:  The type of MRI sequence, such as T1-weighted, T2-weighted, etc.
        created_at:     The timestamp of when the MRI sequence was created.
        updated_at:     The timestamp of when the MRI sequence was last updated.
        tags:   A list of tags or keywords associated with the MRI sequence, useful for
                searching and filtering.
    """

    id: str | None = Field(alias="_id", default=None)
    name: str
    description: str | None = None
    sequence_type: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    tags: list[str] | None = None


# Might be obsolete, to be updated
class DeviceTask(BaseModel):
    """Pydantic model definition of a device workflow."""

    device_id: str
    record_id: UUID
    command: Commands
    parametrized_sequence: ParametrizedSequence


class ScanJob(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic model definition of a scanjob."""

    class Config:
        """Pydantic configuration."""

        extra = Extra.ignore

    job_id: int = Field(alias="id")
    sequence_id: str
    workflow_id: int
    device_id: str


class ScanStatus(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of a scanstatus."""

    record_id: UUID
    status_percent: int


# Obsolete, to be removed
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


class DeviceOut(BaseDevice):
    """Devicee output model."""

    id: str
    datetime_created: datetime
    datetime_updated: datetime | None


class TaskEvent(BaseModel):
    """Task Event."""  # noqa: E501

    task_id: str
    input: dict[str, str]


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
    
    class Config:
        """Base class configuration."""

        # extra = Extra.ignore
        # schema_extra = {
        #     "examples": [
        #         {
        #             "description": "task description",
        #             "type": TaskType.PROCESSING_TASK,
        #             "args": {"arg1": "val1"},
        #             "artifacts": {
        #                 "input": [
        #                     {
        #                         "path": "/data",
        #                         "name": "inputfile2"
        #                     }
        #                 ],
        #                 "output": [
        #                     {
        #                         "path": "/data",
        #                         "name": "outputfile1"
        #                     }
        #                 ]
        #             },
        #             "task_destinations": [],
        #             "status": {TaskStatus.PENDING: "additional status information"}
        #         }
        #     ]
        # }

    workflow_id: Optional[UUID] = None
    name: str
    description: str
    type: TaskType
    args: dict[str, str]
    artifacts: dict[str, str]
    destinations: dict[str, str]
    status: dict[TaskStatus, str]
    is_template: bool
    is_frozen: bool


class TaskOut(BaseTask):
    """Task output model."""

    id: UUID
    datetime_created: datetime


class BaseWorkflow(BaseModel):
    """Workflow base model."""

    class Config:
        """Base class configuration."""

        extra = Extra.ignore

    name: str
    comment: str | None
    exam_id: Optional[UUID] = None
    status: Literal["NEW", "UPDATED", "DELETED"]
    is_finished: bool
    is_template: bool
    is_frozen: bool


class WorkflowOut(BaseWorkflow):
    """Workflow output model."""

    id: UUID
    tasks: list[TaskOut]
    datetime_created: datetime
    datetime_updated: datetime | None


class BaseExam(BaseModel):
    """Exam base model."""

    class Config:
        """Base class configuration."""

        extra = Extra.ignore

    patient_id: Optional[int] = None # TODO: replace by UUID
    name: str
    country: str | None
    site: str | None
    address: str | None
    status: Literal["NEW", "UPDATED", "DELETED"]
    is_template: bool
    is_frozen: bool


class ExamOut(BaseExam):
    """Exam output model."""

    id: UUID
    datetime_created: datetime
    datetime_updated: datetime | None
    workflows: list[WorkflowOut]


class UserRole(Enum):
    admin = "admin"
    medical = "medical"
    scientist = "scientist"
    engineer = "engineer"


class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str | None
    role: UserRole
    # access_token is a standardized name in OAuth2, don't change it
    access_token: str
    # token_type is a standardized name in OAuth2, don't change it
    # token_type should most of the time be "bearer" as standardized in OAuth2
    # when adding new user, token_type is "password" and access_token contains password
    token_type: str     
    last_activity_unixtime: int | None
    last_login_unixtime: int | None


# @dataclass
class BasePatient(BaseModel):
    """Patient pydantic base model."""

    # @dataclass
    class Config:
        """Pydantic model configuration."""

        extra = Extra.ignore
        allow_population_by_field_name = True

    first_name: str
    last_name: str
    birth_date: date
    sex: Gender
    issuer: str
    status: Literal["NEW", "UPDATED", "DELETED"]
    comment: str | None


# @dataclass
class PatientOut(BasePatient):
    """Patient pydantic output model."""

    patient_id: int = Field(alias="id")
    datetime_created: datetime
    datetime_updated: datetime | None
