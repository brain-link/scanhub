"""Workflow manager main."""

from api.db import init_db
from api.workflow import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute


def custom_client_uid(route: APIRoute):
    """Generate custom client id.

    TODO: Update docstring

    Parameters
    ----------
    route
        Api route

    Returns
    -------
        Client uid string
    """
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
    """Call database initialization of startup."""
    init_db()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Skeleton for shutdown routine."""
    pass


@router.get('/health/readiness', response_model={}, status_code=200, tags=['health'])
async def readiness() -> dict:
    """Readiness health endpoint.

    Returns
    -------
        Status dictionary
    """
    return {'status': 'ok'}


app.include_router(router, prefix='/api/v1/workflow', tags=['workflow'])
