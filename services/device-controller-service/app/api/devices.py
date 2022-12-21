from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

from typing import List
import os

import json
from pydantic import BaseModel, StrictStr
from kafka import KafkaProducer

from app.api.models import DeviceOut, DeviceIn, DeviceUpdate
from app.api import db_manager

from scanhub import RecoJob



class AcquisitionEvent:
    def __init__(self, instruction : str):
        self.instruction = instruction


producer = KafkaProducer(bootstrap_servers=['kafka-broker:9093'],
                         value_serializer=lambda x: json.dumps(x.__dict__).encode('utf-8'))


devices = APIRouter()

@devices.post('/', response_model=DeviceOut, status_code=201)
async def create_device(payload: DeviceIn):
    device_id = await db_manager.add_device(payload)

    response = {
        'id': device_id,
        **payload.dict()
    }

    return response

@devices.get('/{id}/', response_model=DeviceOut)
async def get_device(id: int):
    device = await db_manager.get_device(id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@devices.post('/{device_id}/result/{result_id}/')
async def upload_result(device_id: str, result_id: str, file: UploadFile = File(...)):

    filename = f'{device_id}/{result_id}/{file.filename}'

    try:
        contents = file.file.read()
        app_filename = f'/app/data_lake/{filename}'
        os.makedirs(os.path.dirname(app_filename), exist_ok=True)
        with open(app_filename, 'wb') as f:
            f.write(contents)
    except Exception as ex:
        return {"message": "There was an error uploading the file" + str(ex)}
        raise HTTPException(status_code = 500, detail = "")
    finally:
        file.file.close()


    #TODO: switch based on the preselected reco
        
    reco_job = RecoJob(reco_id="cartesian", device_id=device_id, result_id=result_id, input=filename)

    #TODO: On successful upload message kafka the correct topic to do reco

    producer.send('mri_cartesian_reco', reco_job)

    #TODO: On successful upload message kafka topic to do reco
    return {"message": f"Successfully uploaded {file.filename}"}

#TODO: frontend neesds to call a generic endpoint to trigger the acquisition
#@devices.post('/control/{device_id}/{record_id}/{command}')
@devices.post('/control/{command}/')
async def acquistion_control(command: str):
    acquisitionEvent = AcquisitionEvent(command)
    producer.send('acquisitionEvent', acquisitionEvent)
    return {"message": f"Triggered {command}"}

@devices.get('/result/{device_id}/result/{result_id}/')
async def download_result(device_id: str, result_id: str):
    file_name = f'cartesian.dcm'
    file_path = f'/app/data_lake/{device_id}/{result_id}/{file_name}'
    
    return FileResponse(path=file_path, media_type='application/octet-stream', filename=file_name)
