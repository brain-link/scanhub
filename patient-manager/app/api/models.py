"""Patient pydantic models."""

from datetime import datetime

from .db import Patient
from pydantic import BaseModel, Extra


class BasePatient(BaseModel):
    """Patient pydantic base model."""

    class Config:
        """Pydantic model configuration."""

        extra = Extra.ignore

    sex: str
    name: str
    birth_date: str
    issuer: str
    status: str
    comment: str


class PatientOut(BasePatient):
    """Patient pydantic output model."""

    patient_id: int
    datetime_created: datetime
    datetime_updated: datetime | None


async def get_patient_out(data: Patient) -> PatientOut:
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
