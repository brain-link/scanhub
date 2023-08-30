# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Pydantic models of device."""

from datetime import datetime

from api.db import Device
from pydantic import BaseModel  # noqa


class BaseDevice(BaseModel):
    """Device pydantic base model."""

    name: str
    manufacturer: str
    modality: str
    status: str
    site: str | None
    ip_address: str


class DeviceOut(BaseDevice):
    """Device pydantic output model."""

    id: str
    datetime_created: datetime = datetime.now()
    datetime_updated: datetime = datetime.now()


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
        name=data.name,
        manufacturer=data.manufacturer,
        modality=data.modality,
        status=data.status,
        site=data.site,
        ip_address=data.ip_address,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
    )
