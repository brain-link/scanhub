# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Pydantic models of acquisition control."""
# TODO: Add docstrings to all models and fields, such that they can be shown in the OpenAPI documentation
from datetime import date, datetime
from enum import Enum
from uuid import UUID
from typing import Literal, Any

from pydantic import BaseModel, ConfigDict, Field  # noqa


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

    fov_scaling: XYZ
    fov_offset: XYZ
    fov_rotation: XYZ


class AcquisitionLimits(BaseModel):
    """Pydantic definition of AcquisitionLimits."""

    patient_height: int
    patient_weight: int
    patient_gender: Gender = Field(Gender.NOT_GIVEN)
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


class DeviceCreationRequest(BaseModel):
    """
    Device registration request pydantic model
    (to be sent by user first adding the device to the platform).
    """

    model_config = ConfigDict(extra="ignore")

    title: str
    description: str


class DeviceDetails(BaseModel):
    """Device details pydantic model (to be sent by the device)."""

    model_config = ConfigDict(extra="ignore")

    name: str
    manufacturer: str
    modality: str
    status: str
    site: str
    ip_address: str


class DeviceOut(DeviceCreationRequest, DeviceDetails):
    """Device pydantic output model."""

    id: UUID
    datetime_created: datetime
    datetime_updated: datetime | None = None


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

    task_id: UUID | None = None
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
    """Task base model."""

    model_config = ConfigDict(extra="ignore")

    workflow_id: UUID | None = None
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
    datetime_updated: datetime | None = None
    results: list[ResultOut]


class BaseAcquisitionTask(BaseTask):
    """Represents a task for data acquisition in the system."""

    task_type: Literal[TaskType.ACQUISITION]
    device_id: UUID | None = None
    sequence_id: str    # sequence ID is a mongo db ObjectId, which is not a UUID
    acquisition_parameter: AcquisitionParameter


class AcquisitionTaskOut(TaskOut, BaseAcquisitionTask):
    """Acquisition Task output model."""

    acquisition_limits: AcquisitionLimits | None = None


class BaseDAGTask(BaseTask):
    """Workflow task model."""

    task_type: Literal[TaskType.DAG]
    dag_type: Literal[TaskType.RECONSTRUCTION, TaskType.PROCESSING]
    dag_id: str
    input_id: UUID | None = None
    parameter: dict | None = None


class DAGTaskOut(TaskOut, BaseDAGTask):
    """Workflow Task output model."""

    pass


class BaseWorkflow(BaseModel):
    """Workflow base model."""

    model_config = ConfigDict(extra="ignore")

    exam_id: UUID | None = None
    name: str
    description: str
    comment: str | None = None
    status: ItemStatus
    is_template: bool


class WorkflowOut(BaseWorkflow):
    """Workflow output model."""

    id: UUID
    creator: str
    datetime_created: datetime
    datetime_updated: datetime | None = None
    tasks: list[AcquisitionTaskOut | DAGTaskOut]


class BaseExam(BaseModel):
    """Exam base model."""

    model_config = ConfigDict(extra="ignore")

    patient_id: UUID | None = None
    name: str
    description: str
    indication: str | None = None
    comment: str | None = None
    status: ItemStatus
    is_template: bool


class ExamOut(BaseExam):
    """Exam output model."""

    id: UUID
    creator: str
    datetime_created: datetime
    datetime_updated: datetime | None = None
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
    email: str | None = None
    role: UserRole
    # access_token is a standardized name in OAuth2, don't change it
    access_token: str
    # token_type is a standardized name in OAuth2, don't change it
    # token_type should most of the time be "bearer" as standardized in OAuth2
    # when adding new user, token_type is "password" and access_token contains password
    token_type: str
    last_activity_unixtime: int | None = None
    last_login_unixtime: int | None = None


class PasswordUpdateRequest(BaseModel):
    password_of_requester: str                 # the password of the user that sends the request
    username_to_change_password_for: str       # the username of the user whose password is set
    newpassword: str                           # the new password


class BasePatient(BaseModel):
    """Patient pydantic base model."""

    model_config = ConfigDict(extra="ignore")

    first_name: str
    last_name: str
    birth_date: date
    sex: Gender
    height: float
    weight: float
    issuer: str
    status: ItemStatus = ItemStatus.NEW
    comment: str | None = None


class PatientOut(BasePatient):
    """Patient pydantic output model."""

    patient_id: UUID = Field(alias="id")
    datetime_created: datetime
    datetime_updated: datetime | None = None


class BaseMRISequence(BaseModel):
    """Base model for MRI sequence."""

    model_config = ConfigDict(extra="ignore")
    
    name: str
    description: str
    sequence_type: str
    tags: list[str] = []


class MRISequenceOut(BaseMRISequence):
    """Output model for MRI sequence."""

    # Mongo db creates an object _id attribute, which is not a UUID
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime | None = None
    file: Any
    file_extension: str | None = None
