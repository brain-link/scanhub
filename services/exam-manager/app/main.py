from fastapi import FastAPI
from api.exam import exam
from api.db import database

app = FastAPI(openapi_url="/api/v1/exam/openapi.json", docs_url="/api/v1/exam/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(exam, prefix='/api/v1/exam', tags=['exam'])