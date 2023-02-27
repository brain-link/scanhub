from fastapi import FastAPI
from api.workflow import workflow
from api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/workflow/openapi.json", docs_url="/api/v1/workflow/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(workflow, prefix='/api/v1/workflow', tags=['workflow'])