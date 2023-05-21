"""Device manager main."""

from api.db import engine, init_db
from api.devices import router
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from starlette.responses import FileResponse

app = FastAPI(
    openapi_url="/api/v1/device/openapi.json",
    docs_url="/api/v1/device/docs",
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
    """Inititalize database on startup."""
    init_db()


@router.get('/health/readiness', response_model={}, status_code=200, tags=['health'])
async def readiness() -> dict:
    """Readiness health endpoint.

    Inspects sqlalchemy engine and check if workflow table exists.

    Returns
    -------
        Status docstring

    Raises
    ------
    HTTPException
        500: Workflow table not found
    """
    ins = inspect(engine)
    print(f"Found tables: {ins.get_table_names()}")
    if 'device' not in ins.get_table_names():
        raise HTTPException(status_code=500, detail="Could not find device table, table not created.")
    print("Healthcheck: Endpoint is ready.")
    return {'status': 'ok'}


app.include_router(router, prefix='/api/v1/device')
