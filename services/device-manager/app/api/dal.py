# Data Access Layer (DAL)

from sqlalchemy.future import select
from typing import List
from pprint import pprint

from api.models import BaseDevice
from api.db import Device, async_session



async def add_device(payload: BaseDevice) -> Device:
    """Add a new device to the database

    Arguments:
        payload {BaseDevice} -- Pydantic base model to create a new database entry

    Returns:
        Device -- Database orm model
    """
    new_device = Device(**payload.dict())
    async with async_session() as session:
        session.add(new_device)
        await session.commit()
        await session.refresh(new_device)
    # Debug
    print("***** NEW DEVICE *****")
    pprint(new_device.__dict__)
    return new_device


async def get_device(id: int) -> Device:
    """Fetch a device from database

    Arguments:
        id {int} -- Identifier of the device

    Returns:
        Device -- Database orm model
    """
    async with async_session() as session:
        device = await session.get(Device, id)
    return device


async def get_all_devices() -> List[Device]:
    """Get a list of all existing devices

    Returns:
        List[Device] -- List of database orm models
    """
    async with async_session() as session:
        result = await session.execute(select(Device))
        devices = result.scalars().all()
    return devices


async def delete_device(id: int) -> bool:
    """Delete a device by identifier

    Arguments:
        id {int} -- Identifier of the device to be deleted

    Returns:
        bool -- Success of delete event
    """
    async with async_session() as session:
        device = await session.get(Device, id)
        if device:
            await session.delete(device)
            await session.commit()
            return True
        else:
            return False
        
        
async def update_device(id: int, payload: BaseDevice) -> Device:
    """Update an existing device in database

    Arguments:
        id {int} -- Identifier of device
        payload {BaseDevice} -- Pydantic base model, data to be updated

    Returns:
        Device -- Updated database orm model
    """
    async with async_session() as session:
        device = await session.get(Device, id)
        device.update(payload.dict())
        await session.commit()
        await session.refresh(device)
    return device
