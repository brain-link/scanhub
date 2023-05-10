from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from api.db import Device


class BaseDevice(BaseModel):
    name: str
    manufacturer: str
    modality: str
    status: str
    site: Optional[str] = None
    ip_address: str

class DeviceOut(BaseDevice):
    id: int
    datetime_created: datetime
    datetime_updated: Optional[datetime] = None


async def get_device_out(data: Device) -> DeviceOut:
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