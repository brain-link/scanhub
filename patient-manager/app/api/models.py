"""Patient pydantic models."""

from dataclasses import dataclass
from datetime import datetime

import pydantic

from . import db


@dataclass
class BasePatient(pydantic.BaseModel):
    """Patient pydantic base model."""

    @dataclass
    class Config:
        """Pydantic model configuration."""

        extra = pydantic.Extra.ignore

    sex: str
    name: str
    birth_date: str
    issuer: str
    status: str
    comment: str


@dataclass
class PatientOut(BasePatient):
    """Patient pydantic output model."""

    patient_id: int
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
        patient_id=data.patient_id,
        sex=data.sex,
        name=data.name,
        status=data.status,
        comment=data.comment,
        issuer=data.issuer,
        birth_date=data.birth_date,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated
    )
