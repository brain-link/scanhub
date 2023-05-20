"""Exam manager main file."""

from api.db import init_db
from api.exam import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute


def custom_client_uid(route: APIRoute):
    """Generate custom client uid.

    Arguments:
        route -- Api route

    Returns:
        Route string
    """
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    openapi_url="/api/v1/exam/openapi.json",
    docs_url="/api/v1/exam/docs",
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
async def startup():
    """Startup function to initialize DB."""
    init_db()


@app.on_event("shutdown")
async def shutdown():
    """Shutdown function."""
    return


@app.get('/health/readiness', response_model={}, status_code=200)
async def readiness() -> dict:
    """Readiness health endpoint.

    Returns
    -------
        Status dictionary
    """
    return {'status': 'ok'}


app.include_router(router, prefix='/api/v1/exam', tags=['exam'])
