from matplotlib.image import thumbnail
from numpy import rec
from fastapi import APIRouter
from scanhub.models import Patient, Device, Procedures, Recordings, Site, User
from scanhub.utilities.sequence_plot import SequencePlot
import datetime

seq_plot = SequencePlot('/scanhub/scanhub/ressources/epi_pypulseq.seq')

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

@api_router.get("/patients/{patient_id}/procedures/")
async def get_procedures(patient_id: int) -> dict:
    procedures = await Procedures.filter(patient_id=patient_id)
    return procedures

@api_router.get("/patients/{patient_id}/{procedure_id}/records/")
async def get_recordings(procedure_id: int) -> dict:
    records = await Recordings.filter(procedure_id=procedure_id)
    return records

@api_router.post("/patients/{patient_id}/{procedure_id}/records/new/")
async def create_record(record: dict, procedure_id: int) -> str:

    # TODO: Append record to database

    # new_record = await Recordings.create()
    print(record)
    print(f"procedure={procedure_id}")
    
    return "Created new record."

@api_router.get("/patients/{patient_id}/{procedure_id}/records/{record_id}/")
async def get_record(record_id: int) -> dict:
    record = await Recordings.get(id=record_id)
    return record

@api_router.post("/patients/{patient_id}/{procedure_id}/records/{record_id}/sequence/")
async def set_sequence(parameter: list) -> dict:
    for param in parameter:
        print(param)
    return parameter

@api_router.get("/test_sequence/")
async def get_sequence() -> list:
    return seq_plot.get_plot_data()
