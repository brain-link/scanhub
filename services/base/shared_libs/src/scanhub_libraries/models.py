# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Pydantic models of acquisition control."""
from datetime import date, datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, Extra  # noqa


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

    x: float
    y: float
    z: float


class AcquisitionParameter(BaseModel):
    """Pydantic definition of acquisition parameters."""

    fov_scaling: XYZ = XYZ(x=1., y=1., z=1.)
    fov_offset: XYZ = XYZ(x=0., y=0., z=0.)
    fov_rotation: XYZ = XYZ(x=0., y=0., z=0.)


class AcquisitionLimits(BaseModel):
    """Pydantic definition of AcquisitionLimits."""

    patient_height: int
    patient_weight: int
    patient_gender: Gender = Field(None, alias="Gender")
    patient_age: int


# TODO: To be replaced by new acquisition task
class SequenceParameters(BaseModel):
    """Pydantic definition of SequenceParameters."""

    fov: XYZ
    fov_offset: XYZ


# TODO: To be replaced by new acquisition task
class ParametrizedSequence(BaseModel):
    """Pydantic model definition of a parametrized sequence."""

    acquisition_limits: AcquisitionLimits
    sequence_parameters: SequenceParameters
    sequence: str

# TODO: To be replaced by new acquisition task
class DeviceTask(BaseModel):
    """Pydantic model definition of a device workflow."""

    device_id: UUID
    record_id: UUID
    command: Commands
    parametrized_sequence: ParametrizedSequence
    user_access_token: str


# TODO: Needed?
class ScanStatus(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of a scanstatus."""

    record_id: UUID
    status_percent: int


class BaseDevice(BaseModel):
    """Device base model."""

    model_config = ConfigDict(extra=Extra.ignore)

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

    ACQUISITION = "ACQUISITION"
    DAG = "DAG"
    # DAG_TASK has one of the following subtypes
    RECONSTRUCTION = "RECONSTRUCTION"
    PROCESSING = "PROCESSING"


class ResultType(str, Enum):
    """Result type enum."""

    DICOM = "DICOM"
    MRD = "MRD"
    CALIBRATION = "CALIBRATION"

class ItemStatus(str, Enum):
    """Task status enum."""

    NEW = "NEW"
    UPDATED = "UPDATED"
    STARTED = "STARTED"
    FINISHED = "FINISHED"
    DELETED = "DELETED"
    INPROGRESS = "INPROGRESS"


class BaseResult(BaseModel):
    """Result model."""

    task_id: Optional[UUID] = None
    type: ResultType
    status: ItemStatus = ItemStatus.NEW
    directory: str = ""
    filename: str = ""
    progress: float = 0.

class ResultOut(BaseResult):
    """Result output model."""

    id: UUID
    datetime_created: datetime

class BaseTask(BaseModel):
    """Task model."""

    model_config = ConfigDict(extra=Extra.ignore)

    workflow_id: Optional[UUID] = None
    name: str
    description: str
    task_type: TaskType
    destination: str
    status: ItemStatus
    progress: int
    is_template: bool


class TaskOut(BaseTask):
    """Task output model."""

    id: UUID
    creator: str
    datetime_created: datetime
    datetime_updated: datetime | None
    results: list[ResultOut]


class BaseAcquisitionTask(BaseTask):
    """Acquisition task model."""

    task_type: Literal[TaskType.ACQUISITION]
    device_id: UUID
    sequence_id: UUID
    acquisition_parameter: AcquisitionParameter
    acquisition_limits: AcquisitionLimits


class AcquisitionTaskOut(TaskOut, BaseAcquisitionTask):
    """Acquisition Task output model."""

    pass


class BaseDAGTask(BaseTask):
    """Workflow task model."""

    task_type: Literal[TaskType.DAG]
    dag_type: TaskType
    dag_id: str
    input_result_id: UUID | None = None
    parameter: dict | None = None


class DAGTaskOut(TaskOut, BaseDAGTask):
    """Workflow Task output model."""

    pass


class BaseWorkflow(BaseModel):
    """Workflow base model."""

    model_config = ConfigDict(extra=Extra.ignore)

    exam_id: Optional[UUID] = None
    name: str
    description: str
    comment: str | None
    status: ItemStatus
    is_template: bool


class WorkflowOut(BaseWorkflow):
    """Workflow output model."""

    id: UUID
    creator: str
    datetime_created: datetime
    datetime_updated: datetime | None
    tasks: list[AcquisitionTaskOut | DAGTaskOut]


class BaseExam(BaseModel):
    """Exam base model."""

    model_config = ConfigDict(extra=Extra.ignore)

    patient_id: Optional[UUID] = None
    name: str
    description: str
    indication: str | None
    patient_height_cm: int | None
    patient_weight_kg: int | None
    comment: str | None
    status: ItemStatus
    is_template: bool


class ExamOut(BaseExam):
    """Exam output model."""

    id: UUID
    creator: str
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


class PasswordUpdateRequest(BaseModel):
    password_of_requester: str                 # the password of the user that sends the request
    username_to_change_password_for: str       # the username of the user whose password is set
    newpassword: str                           # the new password


class BasePatient(BaseModel):
    """Patient pydantic base model."""

    model_config = ConfigDict(extra=Extra.ignore)

    first_name: str
    last_name: str
    birth_date: date
    sex: Gender
    issuer: str
    status: Literal["NEW", "UPDATED", "DELETED"]
    comment: str | None


class PatientOut(BasePatient):
    """Patient pydantic output model."""

    patient_id: UUID = Field(alias="id")
    datetime_created: datetime
    datetime_updated: datetime | None


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
    tags: list[str] | None = None

