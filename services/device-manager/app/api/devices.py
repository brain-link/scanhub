"""Device api endpoints."""

import json

from api import dal
from api.models import BaseDevice, DeviceOut, get_device_out
from fastapi import APIRouter, HTTPException
from kafka import KafkaProducer

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found


class AcquisitionEvent:
    """Acquisition event class."""

    def __init__(self, instruction: str):
        """Acquisition event constructor.

        Parameters
        ----------
        instruction
            Instructions string
        """
        self.instruction = instruction


producer = KafkaProducer(bootstrap_servers=['kafka-broker:9093'],
                         value_serializer=lambda x: json.dumps(x.__dict__).encode('utf-8'))

router = APIRouter()


@router.get('/health/readiness', response_model={}, status_code=200, tags=['health'])
async def readiness() -> dict:
    """Readiness health endpoint.

    Returns
    -------
        Status dictionary
    """
    return {'status': 'ok'}


@router.post('/', response_model=DeviceOut, status_code=201, tags=["devices"])
async def create_device(payload: BaseDevice) -> DeviceOut:
    """Create new device endpoint.

    Parameters
    ----------
    payload
        Device pydantic base model

    Returns
    -------
        Device pydantic output model

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    if not (device := await dal.device_create(payload)):
        raise HTTPException(status_code=404, detail="Could not create device")
    return await get_device_out(device)


@router.get('/{device_id}', response_model=DeviceOut, status_code=200, tags=["devices"])
async def get_device(device_id: int):
    """Get device endpoint.

    Parameters
    ----------
    device_id
        Id of requested device

    Returns
    -------
        Device pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    if not (device := await dal.device_get(device_id)):
        raise HTTPException(status_code=404, detail="Device not found")
    return await get_device_out(device)


@router.get('/', response_model=list[DeviceOut], status_code=200, tags=["devices"])
async def get_devices() -> list[DeviceOut]:
    """Get all devices endpoint.

    Returns
    -------
        List of device pydantic output models
    """
    if not (devices := await dal.get_all_devices()):
        # Don't raise exception here, list might be empty
        return []
    return [await get_device_out(device) for device in devices]


@router.delete('/{device_id}', response_model={}, status_code=204, tags=["devices"])
async def delete_device(device_id: int):
    """Delete device endpoint.

    Parameters
    ----------
    device_id
        Id of device to be deleted

    Raises
    ------
    HTTPException
        404: Not found
    """
    if not await dal.delete_device(device_id):
        raise HTTPException(status_code=404, detail="Device not found")


@router.put('/{device_id}', response_model=DeviceOut, status_code=200, tags=["devices"])
async def update_device(device_id: int, payload: BaseDevice):
    """Update device endpoint.

    Parameters
    ----------
    device_id
        Id of device to be updated
    payload
        New device pydantic base model, contains new data

    Returns
    -------
        Updated device pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    if not (device := await dal.update_device(device_id, payload)):
        raise HTTPException(status_code=404, detail="Device not found")
    return await get_device_out(device)
