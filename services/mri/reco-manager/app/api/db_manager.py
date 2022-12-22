from app.api.models import RecoIn, RecoOut, RecoUpdate
from app.api.db import recos, database


async def add_reco(payload: RecoIn):
    query = recos.insert().values(**payload.dict())

    return await database.execute(query=query)

async def get_all_recos():
    query = recos.select()
    return await database.fetch_all(query=query)

async def get_reco(id):
    query = recos.select(recos.c.id==id)
    return await database.fetch_one(query=query)

async def delete_reco(id: int):
    query = recos.delete().where(recos.c.id==id)
    return await database.execute(query=query)

async def update_reco(id: int, payload: RecoIn):
    query = (
        recos
        .update()
        .where(recos.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)