# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Patient pydantic models."""

# from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel, Field, Extra

from . import db


# @dataclass
class BasePatient(BaseModel):
    """Patient pydantic base model."""

    # @dataclass
    class Config:
        """Pydantic model configuration."""

        extra = Extra.ignore
        allow_population_by_field_name = True

    sex: str
    name: str
    birth_date: str
    issuer: str
    status: str
    comment: str


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
        sex=data.sex,
        name=data.name,
        status=data.status,
        comment=data.comment,
        issuer=data.issuer,
        birth_date=data.birth_date,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated
    )
