import json

from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from kafka import KafkaProducer

from api.models import BaseDevice, DeviceOut, get_device_out
from api import dal
# from scanhub import RecoJob


# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found


class AcquisitionEvent:
    def __init__(self, instruction : str):
        self.instruction = instruction


producer = KafkaProducer(bootstrap_servers=['kafka-broker:9093'],
                         value_serializer=lambda x: json.dumps(x.__dict__).encode('utf-8'))


devices = APIRouter()


@devices.post('/{id}/', response_model=DeviceOut, status_code=201, tags=["devices"])
async def create_device(payload: BaseDevice):
    device = await dal.add_device(payload)
    if not device:
        raise HTTPException(status_code=404, detail="Could not create device")
    return await get_device_out(device)
    

@devices.get('/{id}/', response_model=DeviceOut, status_code=200, tags=["devices"])
async def get_device(id: int):
    device = await dal.get_device(id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return await get_device_out(device)


@devices.get('/devices/', response_model=list[DeviceOut], status_code=200, tags=["devices"])
async def get_devices() -> list[DeviceOut]:
    devices = await dal.get_all_devices()
    if not devices:
        raise HTTPException(status_code=404, detail="No devices found")
    return [await get_device_out(device) for device in devices]


@devices.delete('/{id}/', response_model={}, status_code=204, tags=["devices"])
async def delete_device(id: int):
    if not await dal.delete_device(id):
        raise HTTPException(status_code=404, detail="Device not found")


@devices.put('/{id}/', response_model=DeviceOut, status_code=200, tags=["devices"])
async def update_device(id: int, payload: BaseDevice):
    device = await dal.update_device(id, payload)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return await get_device_out(device)