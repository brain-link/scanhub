# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Data Access Layer (DAL)."""

from pprint import pprint

from sqlalchemy.future import select

from .db import Patient, async_session
from .models import BasePatient


async def add_patient(payload: BasePatient) -> Patient:
    """Create a new patient entry in database.

    Parameters
    ----------
    payload
        Patient pydantic base model

    Returns
    -------
        Patient database entry
    """
    # TODO verify payload.issuer
    new_patient: Patient = Patient(**payload.dict())
    async with async_session() as session:
        session.add(new_patient)
        await session.commit()
        await session.refresh(new_patient)
    print("***** NEW PATIENT ******")
    pprint(new_patient.__dict__)
    return new_patient


async def get_patient(patient_id: int) -> (Patient | None):
    """Fetch a patient from database.

    Parameters
    ----------
    patient_id
        Id of the requested patient

    Returns
    -------
        Patient database entry
    """
    async with async_session() as session:
        patient = await session.get(Patient, patient_id)
    return patient


async def get_all_patients() -> list[Patient]:
    """Get a list of all existing patients.

    Returns
    -------
        List of database orm models
    """
    async with async_session() as session:
        result = await session.execute(select(Patient))
        patients = list(result.scalars().all())
    return patients


async def delete_patient(patient_id: int) -> bool:
    """Delete patient entry from database.

    Parameters
    ----------
    patient_id
        Id of the patient to be deleted

    Returns
    -------
        Delete success
    """
    async with async_session() as session:
        if (patient := await session.get(Patient, patient_id)):
            await session.delete(patient)
            await session.commit()
            return True
        return False


async def update_patient(patient_id: int, payload: BasePatient) -> (Patient | None):
    """Update existing patient in database.

    Parameters
    ----------
    patient_id
        Id of the patient to be updated

    Returns
    -------
        Updated database entry
    """
    # TODO verify payload.issuer
    async with async_session() as session:
        if (patient := await session.get(Patient, patient_id)):
            patient.update(payload)
            await session.commit()
            await session.refresh(patient)
            return patient
        return None
