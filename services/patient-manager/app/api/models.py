# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Patient pydantic models."""

# from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Extra, Field
from scanhub_libraries.models import Gender

from . import db


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


async def get_patient_out(data: db.Patient) -> PatientOut:
    """Get pydantic output model from database ORM model.

    Parameters
    ----------
    data
        Database ORM model

    Returns
    -------
        Pydantic output model
    """
    return PatientOut(
        id=data.patient_id,
        first_name=data.first_name,
        last_name=data.last_name,
        birth_date=data.birth_date,
        sex=data.sex,
        issuer=data.issuer,
        status=data.status,
        comment=data.comment,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated
    )
