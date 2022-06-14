from fastapi import APIRouter
from scanhub.models import Patient, Device


# Define an api router
api_router = APIRouter()


@api_router.get("/")
async def root() -> dict:
    return dict(
        msg="Hello World!"
    )

# Patient table data
@api_router.get("/patients/")
async def get_patients() -> dict:
    patients = await Patient.all()
    return patients

# Get a certain patient by id
@api_router.get("/patients/{patient_id}/")
async def get_patient(patient_id: int) -> dict:
    patient = await Patient.get(id=patient_id)
    return patient

# TODO: Should we do it like this or just return whats in the database?
# -> Interface mapping could be performed on the frontend side

    # return [dict(
    #     id=patient.id,
    #     sex=patient.sex,
    #     birthday=patient.birthday,
    #     concern=patient.concern,
    #     status=patient.status
    # ) for patient in patients]

# Device table data
@api_router.get("/devices/")
async def get_devices() -> dict:
    devices = await Device.all()
    return devices


