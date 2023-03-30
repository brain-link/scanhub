# Data Access Layer (DAL)

from sqlalchemy.future import select
from typing import List
from pprint import pprint

from api.models import BasePatient
from api.db import Patient, async_session



async def add_patient(payload: BasePatient) -> Patient:
    """Add a new patient to the database

    Arguments:
        payload {BasePatient} -- Pydantic base model to create a new database entry

    Returns:
        Patient -- Database orm model
    """
    new_patient = Patient(**payload.dict())
    async with async_session() as session:
        session.add(new_patient)
        await session.commit()
        await session.refresh(new_patient)
    print("***** NEW PATIENT ******")
    pprint(new_patient.__dict__)
    return new_patient


async def get_patient(id: int) -> Patient:
    """Fetch a patient from database

    Arguments:
        id {int} -- ID of patient

    Returns:
        Patient -- Database orm model
    """
    async with async_session() as session:
        patient = await session.get(Patient, id)
    return patient


async def get_all_patients() -> List[Patient]:
    """Get a list of all existing patients

    Returns:
        List[Patient] -- List of database orm models
    """
    async with async_session() as session:
        result = await session.execute(select(Patient))
        patients = result.scalars().all()
    return patients


async def delete_patient(id: int) -> bool:
    """Delete a patient by ID

    Arguments:
        id {int} -- ID of patient to be deleted

    Returns:
        bool -- Success of delete event
    """
    async with async_session() as session:
        patient = await session.get(Patient, id)
        if patient:
            await session.delete(patient)
            await session.commit()
            return True
        else:
            return False
        

async def update_patient(id: int, payload: BasePatient) -> Patient:
    """Update an existing patient in database

    Arguments:
        id {int} -- ID of patient
        payload {BasePatient} -- Pydantic model, data to be updated

    Returns:
        Patient -- Updated database orm model
    """
    async with async_session() as session:
        patient = await session.get(Patient, id)
        if patient:
            patient.update(payload.dict())
            await session.commit()
            await session.refresh(patient)
            return patient
        else:
            return None
