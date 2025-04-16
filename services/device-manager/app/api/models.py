# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Pydantic models of device."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel  # noqa

from api.db import Device


class DeviceDetails(BaseModel):
    """Device details pydantic model (to be sent by the device)."""

    name: str
    manufacturer: str
    modality: str
    status: str
    site: str
    ip_address: str


class DeviceCreationRequest(BaseModel):
    """Device registration request pydantic model (to be sent by user first adding the device to the platform)."""

    title: str
    description: str


class DeviceOut(BaseModel):
    """Device pydantic output model."""

    id: UUID
    datetime_created: datetime
    datetime_updated: datetime | None

    # attributes from DeviceCreationRequest
    title: str
    description: str

    # attributes from DeviceDetails
    status: str
    name: str | None
    manufacturer: str | None
    modality: str | None
    site: str | None
    ip_address: str | None


async def get_device_out(data: Device) -> DeviceOut:
    """Get pydantic device output model helper function.

    Parameters
    ----------
    data
        Database model

    Returns
    -------
        Pydantic output model
    """
    return DeviceOut(
        id=data.id,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,

        name=data.name,
        manufacturer=data.manufacturer,
        modality=data.modality,
        status=data.status,
        site=data.site,
        ip_address=data.ip_address,

        title=data.title,
        description=data.description
    )
