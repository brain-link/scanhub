# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""API file for the MRI sequence manager service."""

from fastapi import APIRouter, HTTPException

from api.models import SequenceOut, SequenceIn, SequenceUpdate
from api import db_manager
from api.service import is_device_present

sequences = APIRouter()

### NEW API

@sequences.get('/list', response_model=list[SequenceOut])
async def get_sequence_list():
    return await db_manager.get_all_sequences()

@sequences.get('/{id}/', response_model=SequenceOut)
async def get_sequence(id: int):
    sequence = await db_manager.get_sequence(id)
    if not sequence:
        raise HTTPException(status_code=404, detail="Sequence not found")
    return sequence

@sequences.get('/compile')#, response_model=.seq)
async def compile_sequence():
    #TBD: compile the sequence
    return

@sequences.upload('/upload')
async def upload_sequence():
    #TBD: upload the sequence
    return


### OLD API

@sequences.post('/', response_model=SequenceOut, status_code=201)
async def create_sequence(payload: SequenceIn):
    for device_id in payload.devices_id:
        if not is_device_present(device_id):
            raise HTTPException(status_code=404, detail=f"Device with given id:{device_id} not found")

    sequence_id = await db_manager.add_sequence(payload)
    response = {
        'id': sequence_id,
        **payload.dict()
    }

    return response

@sequences.get('/', response_model=list[SequenceOut])
async def get_sequences():
    return await db_manager.get_all_sequences()

@sequences.put('/{id}/', response_model=SequenceOut)
async def update_sequence(id: int, payload: SequenceUpdate):
    sequence = await db_manager.get_sequence(id)
    if not sequence:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)

    if 'devices_id' in update_data:
        for device_id in payload.devices_id:
            if not is_device_present(device_id):
                raise HTTPException(status_code=404, detail=f"Device with given id:{device_id} not found")

    sequence_in_db = SequenceIn(**sequence)

    updated_sequence = sequence_in_db.copy(update=update_data)

    return await db_manager.update_sequence(id, updated_sequence)

@sequences.delete('/{id}/', response_model=None)
async def delete_sequence(id: int):
    sequence = await db_manager.get_sequence(id)
    if not sequence:
        raise HTTPException(status_code=404, detail="Sequence not found")
    return await db_manager.delete_sequence(id)
