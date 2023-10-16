# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Pydantic models of acquisition control."""

from pydantic import BaseModel, Extra, Field  # noqa
from enum import Enum


class Gender(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'
    not_given = 'not_given'


class Commands(str, Enum):
    start = 'start'
    stop = 'stop'
    pause = 'pause'


class XYZ(BaseModel):
    x: float
    y: float
    z: float


class AcquisitionLimits(BaseModel):
    patient_height: float
    patient_weight: float
    patient_gender: Field(None, alias='Gender')
    patient_age: int


class SequenceParameters(BaseModel):
    fov: XYZ
    fov_offset: XYZ


class ScanJob(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic model definition of a scanjob."""

    class Config:
        """Pydantic configuration."""

        extra = Extra.ignore

    job_id: int = Field(alias="id")
    sequence_id: str
    workflow_id: int
    device_id: str
    acquisition_limits: AcquisitionLimits
    sequence_parameters: SequenceParameters


class ParametrizedSequence:
    acquisition_limits: AcquisitionLimits
    sequence_parameters: SequenceParameters
    sequence: str


class DeviceTask:
    device_id: str
    record_id: str
    command: Commands
    parametrized_sequence: ParametrizedSequence


class ScanStatus(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of a scanjob."""

    record_id: str
    status_percent: int


class ScanRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of data to receive."""

    record_id: str
