from fastapi import FastAPI
from fastapi.routing import APIRoute

from api.exam import exam
from api.db import init_db


def custom_client_uid(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    openapi_url="/api/v1/exam/openapi.json", 
    docs_url="/api/v1/exam/docs",
    generate_unique_id_function=custom_client_uid,
)

@app.on_event("startup")
async def startup():
    init_db()

@app.on_event("shutdown")
async def shutdown():
    pass

app.include_router(exam, prefix='/api/v1/exam', tags=['exam'])