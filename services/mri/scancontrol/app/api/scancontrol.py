from typing import List
from fastapi import APIRouter, HTTPException

from api.models import RecordIDList, Procedure, Record, Status
from api.service import is_device_present

import uuid

scancontrol = APIRouter()

@scancontrol.post('/start-procedure', response_model=RecordIDList, status_code=201)
async def start_procedure(payload: Procedure):

    record_id_list = RecordIDList(procedure_id=payload.id, id_list=[])

    for record in payload.records:
        record_id = create_record(record)
        record_id_list.id_list.append(record_id)

    return record_id_list


@scancontrol.post('/start-record', response_model=str, status_code=201)
async def start_record(payload: Record):
    record_id = create_record(payload)

    return record_id

async def create_record(record: Record):
    record_id = str(uuid.uuid4())

    #TBD: create record directory in the datalake
    #TBD: Parametrize the sequence

    return record_id

@scancontrol.post('/stop-record/{record_id}', status_code=201)
async def stop_record(record_id: str):
    #TBD: stop the sequence

    return

@scancontrol.post('/status/{record_id}', status_code=201)
async def set_status(payload: Status, record_id: str):
    #TBD: set the status of the record

    return

@scancontrol.get('/status/{record_id}', response_model=Status, status_code=201)
async def get_status(record_id: str):
    #TBD: get the status of the record

    return Status(id=record_id, status='')