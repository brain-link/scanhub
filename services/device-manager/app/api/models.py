"""Pydantic models of device."""

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
