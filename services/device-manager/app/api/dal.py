# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Device data access layer."""

from pprint import pprint

from api.db import Device, async_session
from api.models import BaseDevice
from sqlalchemy.engine import Result
from sqlalchemy.future import select


async def dal_create_device(payload: BaseDevice) -> Device:
    """Add a new device to the database.

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


async def dal_get_device(device_id: int) -> (Device | None):
    """Fetch a device from database.

    Arguments:
        device_id {int} -- Identifier of the device

    Returns:
        Device -- Database orm model
    """
    async with async_session() as session:
        device = await session.get(Device, device_id)
    return device


async def dal_get_all_devices() -> list[Device]:
    """Get a list of all existing devices.

    Returns:
        List[Device] -- List of database orm models
    """
    async with async_session() as session:
        result: Result = await session.execute(select(Device))
        devices = list(result.scalars().all())
    return devices


async def dal_delete_device(device_id: int) -> bool:
    """Delete a device by identifier.

    Arguments:
        device_id {int} -- Identifier of the device to be deleted

    Returns:
        bool -- Success of delete event
    """
    async with async_session() as session:
        if device := await session.get(Device, device_id):
            await session.delete(device)
            await session.commit()
            return True
        return False


async def dal_update_device(device_id: int, payload: BaseDevice) -> (Device | None):
    """Update an existing device in database.

    Arguments:
        id {int} -- Identifier of device
        payload {BaseDevice} -- Pydantic base model, data to be updated

    Returns:
        Device -- Updated database orm model
    """
    async with async_session() as session:
        if device := await session.get(Device, device_id):
            device.update(payload.dict())
            await session.commit()
            await session.refresh(device)
            return device
        return None
