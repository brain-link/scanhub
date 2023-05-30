#!/usr/bin/env python3

# Project: ScanHub
# File: dal.py
# Date: June 2023
#
# License:
# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
#
# SPDX-License-Identifier: GPL-3.0-only OR ScanHub commercial license
#
# Licensees holding valid ScanHub commercial licenses may use this file in
# accordance with the ScanHub Commercial License Agreement provided with the
# Software or, alternatively, in accordance with the GPL-3.0-only as published
# by the Free Software Foundation. Please refer to the License for the
# specific language governing the rights and limitations under either license.
#
# Brief: Device data access layer.

from pprint import pprint

from api.db import Device, async_session
from api.models import BaseDevice
from sqlalchemy.engine import Result
from sqlalchemy.future import select


async def device_create(payload: BaseDevice) -> Device:
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


async def device_get(device_id: int) -> (Device | None):
    """Fetch a device from database.

    Arguments:
        device_id {int} -- Identifier of the device

    Returns:
        Device -- Database orm model
    """
    async with async_session() as session:
        device = await session.get(Device, device_id)
    return device


async def get_all_devices() -> list[Device]:
    """Get a list of all existing devices.

    Returns:
        List[Device] -- List of database orm models
    """
    async with async_session() as session:
        result: Result = await session.execute(select(Device))
        devices = list(result.scalars().all())
    return devices


async def delete_device(device_id: int) -> bool:
    """Delete a device by identifier.

    Arguments:
        device_id {int} -- Identifier of the device to be deleted

    Returns:
        bool -- Success of delete event
    """
    async with async_session() as session:
        if (device := await session.get(Device, device_id)):
            await session.delete(device)
            await session.commit()
            return True
        return False


async def update_device(device_id: int, payload: BaseDevice) -> (Device | None):
    """Update an existing device in database.

    Arguments:
        id {int} -- Identifier of device
        payload {BaseDevice} -- Pydantic base model, data to be updated

    Returns:
        Device -- Updated database orm model
    """
    async with async_session() as session:
        if (device := await session.get(Device, device_id)):
            device.update(payload.dict())
            await session.commit()
            await session.refresh(device)
            return device
        return None
