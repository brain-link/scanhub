from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

from typing import List
import os

import uuid

import json
from pydantic import BaseModel, StrictStr
from kafka import KafkaProducer

from app.api.models import WorkflowOut, WorkflowIn, WorkflowUpdate
from app.api import db_manager

from scanhub import RecoJob, AcquisitionEvent, AcquisitionCommand


producer = KafkaProducer(bootstrap_servers=['kafka-broker:9093'],
                         value_serializer=lambda x: json.dumps(x.__dict__).encode('utf-8'))


workflow = APIRouter()

@workflow.post('/', response_model=WorkflowOut, status_code=201)
async def create_workflow(payload: WorkflowIn):
    workflow_id = await db_manager.add_workflow(payload)

    response = {
        'id': workflow_id,
        **payload.dict()
    }

    return response

@workflow.get('/{id}/', response_model=WorkflowOut)
async def get_workflow(id: int):
    workflow = await db_manager.get_workflow(id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Device not found")
    return workflow
   
@workflow.post('/{device_id}/result/{result_id}/')
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

#EXAMPLE: http://localhost:8080/api/v1/workflow/control/start/
#TODO: frontend neesds to call a generic endpoint to trigger the acquisition
#@workflow.post('/control/{device_id}/{record_id}/{command}')
@workflow.post('/control/{command}/')
async def acquistion_control(command: str):
    try:
        acquisition_command = AcquisitionCommand[command]
    except KeyError:
        print('KeyError: acquisition command not found')

    record_id = uuid.uuid4() #DEBUG: this should be the record_id from the frontend

    acquisition_event = AcquisitionEvent(device_id='device_id', record_id=record_id, instruction=acquisition_command,input_sequence='input_sequence')
    producer.send('acquisitionEvent', acquisition_event)
    return {"message": f"Triggered {acquisition_event}"}

@workflow.get('/result/{device_id}/result/{result_id}/')
async def download_result(device_id: str, result_id: str):
    file_name = f'cartesian.dcm'
    file_path = f'/app/data_lake/{device_id}/{result_id}/{file_name}'
    
    return FileResponse(path=file_path, media_type='application/octet-stream', filename=file_name)
