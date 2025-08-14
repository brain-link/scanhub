# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Exam manager main file."""


from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.exam_api import exam_router
from app.api.mri_sequence_api import seq_router
from app.api.result_api import result_router
from app.api.task_api import task_router
from app.api.workflow_api import workflow_router
from app.db.mongodb import close_mongo_connection, connect_to_mongo, db
from app.db.postgres import engine, init_db

from . import LOG_CALL_DELIMITER

# To be done: Specify specific origins:
#   Wildcard ["*"] excludes eeverything that involves credentials
#   Better specify explicitly the allowed origins
#   See: https://fastapi.tiangolo.com/tutorial/cors/
ORIGINS = [
    # "http://localhost",       # frontend via nginx-proxy with default port
    # "https://localhost",      # frontend via nginx-proxy with default port
    "http://localhost:8080",    # frontend via nginx-proxy with custom port
    "https://localhost:8443",   # frontend via nginx-proxy with custom port
    "https://localhost:3000",
]


app = FastAPI(
    openapi_url="/api/v1/exam/openapi.json",
    docs_url="/api/v1/exam/docs"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Range"],
    expose_headers=["Content-Range", "Accept-Ranges", "Content-Length"],
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
    """Statup exam-tree microservice.

    Raises
    ------
    HTTPException
        500: Device table does not exist
    HTTPException
        500: Workflow table does not exist
    """
    ins = inspect(engine)
    tables = ins.get_table_names()
    if "device" not in tables:
        raise HTTPException(
            status_code=500,
            detail="SQL-DB: Device table is required but does not exist.",
        )
    print("Initializing postgres db...")
    init_db()
    print("Connecting to mongodb...")
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown function."""
    print("Closing mongodb connection...")
    await close_mongo_connection()
    return None


@app.get("/api/v1/exam/health/readiness", response_model={}, status_code=200, tags=["health"])
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
    print(LOG_CALL_DELIMITER)
    ins = inspect(engine)
    existing_tables = ins.get_table_names()
    required_tables = ["exam", "workflow", "task"]
    # required_tables = ["exam", "workflow", "task", "device"]

    if not all(t in existing_tables for t in required_tables):
        raise HTTPException(status_code=500, detail="SQL-DB: Could not create all required tables.")

    # Check mongo db status
    if db.collection is None:
        raise HTTPException(status_code=503, detail=f"Database not connected: {str(db.collection)}")

    return {"status": "ok"}


app.include_router(exam_router, prefix="/api/v1/exam")
app.include_router(workflow_router, prefix="/api/v1/exam")
app.include_router(task_router, prefix="/api/v1/exam")
app.include_router(result_router, prefix="/api/v1/exam")
app.include_router(seq_router, prefix="/api/v1/exam")
