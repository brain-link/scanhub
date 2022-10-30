from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import MovieOut, MovieIn, MovieUpdate
from app.api import db_manager
from app.api.service import is_device_present

recos = APIRouter()

@recos.post('/', response_model=MovieOut, status_code=201)
async def create_reco(payload: MovieIn):
    for device_id in payload.devices_id:
        if not is_device_present(device_id):
            raise HTTPException(status_code=404, detail=f"Device with given id:{device_id} not found")

    reco_id = await db_manager.add_reco(payload)
    response = {
        'id': reco_id,
        **payload.dict()
    }

    return response

@recos.get('/', response_model=List[MovieOut])
async def get_recos():
    return await db_manager.get_all_recos()

@recos.get('/{id}/', response_model=MovieOut)
async def get_reco(id: int):
    reco = await db_manager.get_reco(id)
    if not reco:
        raise HTTPException(status_code=404, detail="Movie not found")
    return reco

@recos.put('/{id}/', response_model=MovieOut)
async def update_reco(id: int, payload: MovieUpdate):
    reco = await db_manager.get_reco(id)
    if not reco:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)

    if 'devices_id' in update_data:
        for device_id in payload.devices_id:
            if not is_device_present(device_id):
                raise HTTPException(status_code=404, detail=f"Device with given id:{device_id} not found")

    reco_in_db = MovieIn(**reco)

    updated_reco = reco_in_db.copy(update=update_data)

    return await db_manager.update_reco(id, updated_reco)

@recos.delete('/{id}/', response_model=None)
async def delete_reco(id: int):
    reco = await db_manager.get_reco(id)
    if not reco:
        raise HTTPException(status_code=404, detail="Reco not found")
    return await db_manager.delete_reco(id)
