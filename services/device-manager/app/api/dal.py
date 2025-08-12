"""
Device data access layer.

Provides functions to interact with the device database, including creating,
updating, retrieving, and deleting device records. It uses SQLAlchemy for
asynchronous database operations and Pydantic models for data validation.

Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
"""
from uuid import UUID

from scanhub_libraries.models import DeviceCreationRequest
from sqlalchemy.engine import Result
from sqlalchemy.future import select

from app.api.db import Device, async_session


async def dal_create_device(request: DeviceCreationRequest, token_hash: str, salt: str) -> Device:
    """Add a new device to the database.

    Arguments
    ---------
        payload {BaseDevice} -- Pydantic base model to create a new database entry

    """
    new_device = Device(
        **request.model_dump(),
        token_hash=token_hash,
        salt=salt,
    )
    async with async_session() as session:
        session.add(new_device)
        await session.commit()
        await session.refresh(new_device)
    return new_device


async def dal_get_device(device_id: UUID) -> (Device | None):
    """Fetch a device from database.

    Arguments
    ---------
        device_id {UUID} -- Identifier of the device

    Returns
    -------
        Device -- Database orm model
    """
    async with async_session() as session:
        device = await session.get(Device, device_id)
    return device


async def dal_get_all_devices() -> list[Device]:
    """Get a list of all existing devices.

    Returns
    -------
        List[Device] -- List of database orm models
    """
    async with async_session() as session:
        result: Result = await session.execute(select(Device))
        devices = list(result.scalars().all())
    return devices


async def dal_delete_device(device_id: UUID) -> bool:
    """Delete a device by identifier.

    Parameters
    ----------
        device_id {UUID} -- Identifier of the device to be deleted

    Returns
    -------
        bool -- Success of delete event
    """
    async with async_session() as session:
        if device := await session.get(Device, device_id):
            await session.delete(device)
            await session.commit()
            return True
        return False


async def dal_update_device(device_id: UUID, payload: dict) -> (Device | None):
    """Update an existing device in database.

    Parameters
    ----------
        id {UUID} -- Identifier of device
        payload {dict} -- Dict with the fields to update.

    Returns
    -------
        Device -- Updated database orm model.
    """
    async with async_session() as session:
        if device := await session.get(Device, device_id):
            device.update(payload)
            await session.commit()
            await session.refresh(device)
            return device
        return None
