from fastapi import APIRouter
from scanhub.models import Patient, Device, Procedures, Recordings, Site, User


# Define an api router
api_router = APIRouter()


@api_router.get("/")
async def root() -> dict:
    return dict(
        msg="Hello World!"
    )

# Device table data
@api_router.get("/devices/")
async def get_devices() -> dict:
    devices = await Device.all()
    return devices

@api_router.get("/devices/{device_id}/")
async def get_device(device_id: int) -> dict:
    device = await Device.get(id=device_id)
    site = await Site.get(id=device.site_id)
    return dict(
        device=device,
        site=site
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

@api_router.get("/patients/{patient_id}/procedures/")
async def get_procedures(patient_id: int) -> dict:
    procedures = await Procedures.filter(patient_id=patient_id)
    return procedures

@api_router.get("/patients/{patient_id}/{procedure_id}/recordings/")
async def get_recordings(patient_id: int, procedure_id: int) -> dict:

    patient = await Patient.get(id=patient_id)
    procedure = await Procedures.get(id=procedure_id)
    recordings = await Recordings.filter(procedure_id=procedure_id)

    return dict(
        patient=patient,
        procedure=procedure,
        recordings=recordings
    )
