from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

import json

from kafka import KafkaProducer

from api.models import BaseWorkflow, WorkflowOut, get_workflow_out
from api import dal

# from scanhub import RecoJob, AcquisitionEvent, AcquisitionCommand

producer = KafkaProducer(
    bootstrap_servers=['kafka-broker:9093'],
    value_serializer=lambda x: json.dumps(x.__dict__).encode('utf-8')
)


workflow = APIRouter()


@workflow.post('/{id}/', response_model=WorkflowOut, status_code=201, tags=["workflow"])
async def create_workflow(payload: BaseWorkflow):
    workflow = await dal.add_workflow(payload)
    if not workflow:
        raise HTTPException(status_code=404, detail="Could not create workflow")
    return await get_workflow_out(workflow)


@workflow.get('/workflows/', response_model=list[WorkflowOut], tags=["workflow"])
async def get_workflow_list() -> list[WorkflowOut]:
    workflows = await dal.get_all_workflows()
    if not workflows:
        raise HTTPException(status_code=404, detail="Workflows not found")
    return [await get_workflow_out(workflow) for workflow in workflows]


@workflow.get('/{id}/', response_model=WorkflowOut, tags=["workflow"])
async def get_workflow(id: int):
    workflow = await dal.get_workflow(id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return await get_workflow_out(workflow)


@workflow.delete('/{id}/', response_model={}, status_code=204, tags=["workflow"])
async def delete_workflow(id: int):
    if not await dal.delete_workflow(id):
        raise HTTPException(status_code=404, detail="Workflow not found")
    

@workflow.put('/{id}/', response_model=WorkflowOut, tags=["workflow"])
async def update_workflow(id: int, payload: BaseWorkflow):
    workflow = await dal.update_workflow(id, payload)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return await get_workflow_out(workflow)






### OLD API

# @workflow.post('/', response_model=WorkflowOut, status_code=201)
# async def create_workflow(payload: WorkflowIn):
#     workflow_id = await db_manager.add_workflow(payload)

#     response = {
#         'id': workflow_id,
#         **payload.dict()
#     }

#     return response

# @workflow.post('/upload/{record_id}/')
# async def upload_result(record_id: str, file: UploadFile = File(...)):

#     filename = f'records/{record_id}/{file.filename}'

#     try:
#         contents = file.file.read()
#         app_filename = f'/app/data_lake/{filename}'
#         os.makedirs(os.path.dirname(app_filename), exist_ok=True)
#         with open(app_filename, 'wb') as f:
#             f.write(contents)
#     except Exception as ex:
#         return {"message": "There was an error uploading the file" + str(ex)}
#         raise HTTPException(status_code = 500, detail = "")
#     finally:
#         file.file.close()


#     #TODO: switch based on the preselected reco
        
#     reco_job = RecoJob(reco_id="cartesian", device_id="TB removed", record_id=record_id, input=filename)

#     #TODO: On successful upload message kafka the correct topic to do reco

#     producer.send('mri_cartesian_reco', reco_job)

#     #TODO: On successful upload message kafka topic to do reco
#     return {"message": f"Successfully uploaded {file.filename}"}

# #EXAMPLE: http://localhost:8080/api/v1/workflow/control/start/
# #TODO: frontend neesds to call a generic endpoint to trigger the acquisition
# #@workflow.post('/control/{device_id}/{record_id}/{command}')
# @workflow.post('/control/{command}/')
# async def acquistion_control(command: str):
#     try:
#         acquisition_command = AcquisitionCommand[command]
#     except KeyError:
#         print('KeyError: acquisition command not found')

#     device_id = 'mri_simulator' #DEBUG: this should be the device_id from the frontend
#     record_id = uuid.uuid4() #DEBUG: this should be the record_id from the frontend
#     input_sequence = 'input_sequence' #DEBUG: this should be the input_sequence from the frontend

#     acquisition_event = AcquisitionEvent(   device_id=device_id,
#                                             record_id=record_id,
#                                             command_id=acquisition_command,
#                                             input_sequence=input_sequence)
#     producer.send('acquisitionEvent', acquisition_event)
#     return {"message": f"Triggered {acquisition_event}"}

# @workflow.get('/download/{record_id}/')
# async def download(record_id: str):
#     file_name = f'cartesian.dcm'
#     file_path = f'/app/data_lake/records/{record_id}/{file_name}'
    
#     return FileResponse(path=file_path, media_type='application/octet-stream', filename=file_name)
