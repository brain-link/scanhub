from statistics import mode
from fastapi import APIRouter, HTTPException
from scanhub.utilities.sequence_plot import SequencePlot
from scanhub import models
seq_plot = SequencePlot('/scanhub/scanhub/ressources/epi_pypulseq.seq')

# Define an api router
api_router = APIRouter()

# Device table data
@api_router.get("/devices")
async def get_devices() -> dict:
    devices = await models.Device.all()
    return devices

@api_router.post("/devices/new")
async def create_device():
    sites = await models.Site.all()
    if len(sites) == 0:
        site = await models.Site.create(
            name="BrainLink",
            city="Berlin",
            country="Germany",
            address="Berliner Str."
        )
        await site.save()
    else:
        site = sites[0]
    device = await models.Device.create(
        site=site,
        modality=0,
        address="0.0.0.1"
    )
    await device.save()
    return device


# Get a device by id
@api_router.get("/devices/{device_id}/")
async def get_device(device_id: int) -> dict:
    device = await models.Device.get(id=device_id)
    site = await models.Site.get(id=device.site_id)
    return dict(
        device=device,
        site=site
    )

# Patient table data
@api_router.get("/patients/")
async def get_patients() -> dict:
    patients = await models.Patient.all()
    return patients

# Create a new patient
@api_router.post("/patients/new")
async def create_patient(patient_data: models.CreatePatient):
    print(patient_data.dict())
    new_patient = await models.Patient.create(
        sex=patient_data.sex,
        birthday=patient_data.birthday,
        concern=patient_data.concern,
    )
    await new_patient.save()
    return new_patient

# Get a patient by id
@api_router.get("/patients/{patient_id}/")
async def get_patient(patient_id: int) -> dict:
    patient = await models.Patient.get(id=patient_id)
    return patient

# Get a list of procedures by patient id
@api_router.get("/patients/{patient_id}/procedures/")
async def get_procedures(patient_id: int) -> dict:
    procedures = await models.Procedures.filter(patient_id=patient_id)
    return procedures

# Create a new procedure
@api_router.post("/patients/{patient_id}/procedures/new/")
async def create_procedure(procedure_data: models.CreateProcedure, patient_id: int):
    
    print(procedure_data.dict())
    patient = await models.Patient.get(id=patient_id)

    new_procedure = await models.Procedures.create(
        reason=procedure_data.reason,
        patient=patient
    )

    await new_procedure.save()
    return new_procedure

# Delete a procedure by id
@api_router.delete("/patients/{patient_id}/{procedure_id}/")
async def delete_procedure(procedure_id: int):
    print(f"Deleting record id={procedure_id}")
    deleted_count = await models.Procedures.filter(id=procedure_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Procedure {procedure_id} not found")
    return models.Status(message=f"Deleted procedure {procedure_id}")

# Get a list of records by procedure id
@api_router.get("/records/{procedure_id}")
async def get_recordings(procedure_id: int) -> dict:
    record_list = await models.Recordings.filter(procedure_id=procedure_id)
    return record_list

# Create a new record
@api_router.post("/patients/{patient_id}/{procedure_id}/records/new")
async def create_record(record_data: models.Create_Record, procedure_id: int) -> None:

    device = await models.Device.get(id=record_data.device_id)
    procedure = await models.Procedures.get(id=procedure_id)

    print("creating record...")
    new_record = await models.Recordings.create(
        comment=record_data.comment,
        data=record_data.data,
        procedure=procedure,
        device=device
    )

    await new_record.save()
    return new_record

# Get a record by id
@api_router.get("/records/{record_id}/")
async def get_record(record_id: int) -> dict:
    record = await models.Recordings.get(id=record_id)
    return record

# Delete a record by id
@api_router.delete("/patients/{patient_id}/{procedure_id}/records/{record_id}/")
async def delete_record(record_id: int) -> dict:
    print(f"Deleting record id={record_id}")
    deleted_count = await models.Recordings.filter(id=record_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found")
    return models.Status(message=f"Deleted record {record_id}")

# Post a sequence update (sequence parameters)
@api_router.post("/patients/{patient_id}/{procedure_id}/records/{record_id}/sequence/")
async def set_sequence(parameter: list) -> dict:
    for param in parameter:
        print(param)
    return parameter

# Placeholder: Get sequence plot data
@api_router.get("/test_sequence/")
async def get_sequence() -> list:
    return seq_plot.get_plot_data()
