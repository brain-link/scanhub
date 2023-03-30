from datetime import datetime
from pydantic import BaseModel, Extra

from api.db import Patient


class BasePatient(BaseModel):
    sex: str
    name: str
    birth_date: str
    issuer: str
    status: str
    comment: str


class PatientOut(BasePatient):
    id: int
    datetime_created: datetime
    datetime_updated: datetime | None


async def get_patient_out(data: Patient) -> PatientOut:
    return PatientOut(
        id=data.id,
        sex=data.sex,
        name=data.name,
        status=data.status,
        comment=data.comment,
        issuer=data.issuer,
        birth_date=data.birth_date,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated
    )