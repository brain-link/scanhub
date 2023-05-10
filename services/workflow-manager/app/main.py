from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

from api.workflow import router
from api.db import init_db


def custom_client_uid(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    openapi_url="/api/v1/workflow/openapi.json", 
    docs_url="/api/v1/workflow/docs",
    generate_unique_id_function=custom_client_uid,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    init_db()

@app.on_event("shutdown")
async def shutdown():
    pass

app.include_router(router, prefix='/api/v1/workflow', tags=['workflow'])