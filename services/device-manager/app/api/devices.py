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
