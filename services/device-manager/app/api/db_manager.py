from api.models import DeviceIn, DeviceOut, DeviceUpdate
from api.db import devices, database


async def add_device(payload: DeviceIn):
    query = devices.insert().values(**payload.dict())

    return await database.execute(query=query)

async def get_device(id):
    query = devices.select(devices.c.id==id)
    return await database.fetch_one(query=query)

async def get_all_devices():
    query = devices.select()
    return await database.fetch_all(query=query)