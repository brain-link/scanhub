from fastapi import APIRouter, HTTPException
from typing import List

from app.api.models import CastOut, CastIn, CastUpdate
from app.api import db_manager

devices = APIRouter()

@devices.post('/', response_model=CastOut, status_code=201)
async def create_device(payload: CastIn):
    device_id = await db_manager.add_device(payload)

    response = {
        'id': device_id,
        **payload.dict()
    }

    return response

@devices.get('/{id}/', response_model=CastOut)
async def get_device(id: int):
    device = await db_manager.get_device(id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device