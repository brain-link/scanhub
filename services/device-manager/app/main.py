# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Main file for the device manager service."""

from app.api.db import engine, init_db
from app.api.device_endpoints import router as http_router
from app.api.device_websocket import router as ws_router
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    openapi_url="/api/v1/device/openapi.json",
    docs_url="/api/v1/device/docs",
)

# To be done: Specify specific origins:
#   Wildcard ["*"] excludes eeverything that involves credentials
#   Better specify explicitly the allowed origins
#   See: https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    # "http://localhost",       # frontend via nginx-proxy with default port
    # "https://localhost",      # frontend via nginx-proxy with default port
    "http://localhost:8080",    # frontend via nginx-proxy with custom port
    "https://localhost:8443",   # frontend via nginx-proxy with custom port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    """
    Add logging for http exceptions.

    https://fastapi.tiangolo.com/tutorial/handling-errors/#reuse-fastapis-exception-handlers
    """
    print(f"{repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    Add logging for fastAPI's automatic input validation exceptions.

    https://fastapi.tiangolo.com/tutorial/handling-errors/#reuse-fastapis-exception-handlers
    """
    print(f"{exc}")
    return await request_validation_exception_handler(request, exc)


@app.on_event("startup")
async def startup():
    """Inititalize database on startup."""
    init_db()


@app.get("/api/v1/device/health/readiness", response_model={}, status_code=200, tags=["health"])
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
    # print(f"Found tables: {ins.get_table_names()}")
    if "device" not in ins.get_table_names():
        raise HTTPException(
            status_code=500, detail="Could not find device table, table not created."
        )
    return {"status": "ok"}


app.include_router(http_router, prefix="/api/v1/device")
app.include_router(ws_router, prefix="/api/v1/device")
