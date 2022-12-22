from fastapi import FastAPI
from app.api.devices import devices
from app.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/devices/openapi.json", docs_url="/api/v1/devices/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(devices, prefix='/api/v1/devices', tags=['devices'])