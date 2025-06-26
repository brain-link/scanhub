# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of patient endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from scanhub_libraries.models import BasePatient, PatientOut
from scanhub_libraries.security import get_current_user

from . import dal, db

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


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
        height=data.height,
        weight=data.weight,
        issuer=data.issuer,
        status=data.status,
        comment=data.comment,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated
    )


@router.post("/", response_model=PatientOut, status_code=201, tags=["patients"])
async def create_patient(payload: BasePatient) -> PatientOut:
    """Create new patient database entry.

    Parameters
    ----------
    payload
        Patient pydantic base model

    Returns
    -------
        Patient pydantic output model

    Raises
    ------
    HTTPException
        404: Could not create patient
    """
    patient = await dal.add_patient(payload)
    if not patient:
        raise HTTPException(status_code=404, detail="Could not create patient")
    return await get_patient_out(patient)


@router.get("/{patient_id}", response_model=PatientOut, status_code=200, tags=["patients"])
async def get_patient(patient_id: UUID) -> PatientOut:
    """Get a patient from database by id.

    Parameters
    ----------
    patient_id
        Id of the requested patient

    Returns
    -------
        Patient pydantic output model

    Raises
    ------
    HTTPException
        404: Patient not found
    """
    patient = await dal.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return await get_patient_out(patient)


@router.get('/', response_model=list[PatientOut], status_code=200, tags=["patients"])
async def get_patient_list() -> list[PatientOut]:
    """Get all patients endpoint.

    Returns
    -------
        List of patient pydantic output models
    """
    if not (patients := await dal.get_all_patients()):
        # If return is none, list is empty
        return []
    return [await get_patient_out(patient) for patient in patients]


@router.delete("/{patient_id}", response_model={}, status_code=204, tags=["patients"])
async def delete_patient(patient_id: UUID) -> None:
    """Delete patient from database.

    Parameters
    ----------
    patient_id
        Id of patient to be deleted

    Raises
    ------
    HTTPException
        _description_
    """
    if not await dal.delete_patient(patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")


@router.put("/{patient_id}", response_model=PatientOut, status_code=200, tags=["patients"])
async def update_patient(patient_id: UUID, payload: BasePatient):
    """Update existing patient endpoint.

    Parameters
    ----------
    patient_id
        Id of the patient to be updated
    payload
        Patient data to be updated

    Returns
    -------
        Updated patient pydantic output model

    Raises
    ------
    HTTPException
        404: Patient not found
    """
    if not (patient := await dal.update_patient(patient_id, payload)):
        raise HTTPException(status_code=404, detail="Patient not found")
    return await get_patient_out(patient)
