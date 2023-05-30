#!/usr/bin/env python3

# Project: ScanHub
# File: models.py
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
# Brief: Pydantic models of device.

from datetime import datetime

from api.db import Device
from pydantic import BaseModel


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

    id: int
    datetime_created: datetime
    datetime_updated: datetime | None


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
