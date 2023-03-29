from fastapi import FastAPI
from api.sequences import sequences
from api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/mri/sequences/openapi.json", docs_url="/api/v1/mri/sequences/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(sequences, prefix='/api/v1/mri/sequences', tags=['sequences'])