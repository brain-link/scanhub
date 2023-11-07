# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Pydantic models of acquisition control."""
from typing import Any

from pydantic import BaseModel, Extra, Field, Json  # noqa
from enum import Enum


class Gender(str, Enum):
    """Pydantic definition of genders."""

    male = 'MALE'
    female = 'FEMALE'
    other = 'OTHER'
    not_given = 'NOT_GIVEN'


class Commands(str, Enum):
    """Pydantic definition of a commands."""

    start = 'START'
    stop = 'STOP'
    pause = 'PAUSE'


class XYZ(BaseModel):
    """Pydantic definition of coordinates."""

    x: float
    y: float
    z: float


class AcquisitionLimits(BaseModel):
    """Pydantic definition of AcquisitionLimits."""

    patient_height: float
    patient_weight: float
    patient_gender: Gender = Field(None, alias='Gender')
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

    job_id: int = Field(alias="id")
    sequence_id: str
    workflow_id: int
    device_id: str
    acquisition_limits: AcquisitionLimits
    sequence_parameters: SequenceParameters


class ParametrizedSequence(BaseModel):
    acquisition_limits: AcquisitionLimits
    sequence_parameters: SequenceParameters
    sequence: Json[Any]


class DeviceTask(BaseModel):
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
