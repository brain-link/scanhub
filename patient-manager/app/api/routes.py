"""Definition of patient endpoints."""
from fastapi import APIRouter, HTTPException

from . import dal
from .models import BasePatient, PatientOut, get_patient_out


router = APIRouter()


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
async def get_patient(patient_id: int) -> PatientOut:
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
async def delete_patient(patient_id: int) -> None:
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
async def update_patient(patient_id: int, payload: BasePatient):
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
