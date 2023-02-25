from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import RecordIDList, Procedure, Record
from app.api.service import is_device_present

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


def create_record(record: Record):
    record_id = str(uuid.uuid4())

    #TBD: create record directory in the datalake
    #TBD: Parametrize the sequence

    return record_id
