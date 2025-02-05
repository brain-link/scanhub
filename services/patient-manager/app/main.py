# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Patient manager main file."""

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.db import engine, init_db
from api.routes import router

app = FastAPI(
    openapi_url="/api/v1/patient/openapi.json",
    docs_url="/api/v1/patient/docs",
    title="ScanHub-UI"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
async def startup() -> None:
    """Initialize patient database."""
    init_db()


@app.get("/api/v1/patient/health/readiness", response_model={}, status_code=200, tags=["health"])
async def readiness() -> dict:
    """Readiness health endpoint.

    Returns
    -------
        Status dictionary

    Raises
    ------
    HTTPException
        500: Any of the exam-tree tables does not exist
    """
    ins = inspect(engine)
    existing_tables = ins.get_table_names()
    required_tables = ["patients"]

    if not all(t in existing_tables for t in required_tables):
        raise HTTPException(status_code=500, detail="SQL-DB: Could not create all required tables.")

    return {"status": "ok"}


app.include_router(router, prefix="/api/v1/patient")
