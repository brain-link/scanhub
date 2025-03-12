# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Exam manager main file."""


from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.responses import FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import LOG_CALL_DELIMITER
from app.db import engine, init_db
from app.api.exam_api import exam_router
from app.api.result_api import result_router
from app.api.workflow_api import workflow_router
from app.api.task_api import task_router
from app.dal import result_dal
from uuid import UUID
import os
import shutil

# To be done: Specify specific origins:
#   Wildcard ["*"] excludes eeverything that involves credentials
#   Better specify explicitly the allowed origins
#   See: https://fastapi.tiangolo.com/tutorial/cors/
ORIGINS = [
    "http://localhost",
    "http://localhost:3000",  # frontned
    "http://localhost:8100",  # patient-manager
    "http://localhost:8080",  # nginx
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
    init_db()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown function."""
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

    return {"status": "ok"}

@app.get("/api/v1/exam/dicom/{result_id}", response_class=FileResponse, status_code=200, tags=["results"])
async def get_dicom(result_id: UUID | str) -> FileResponse:
    print(LOG_CALL_DELIMITER)
    print("result_id:", result_id)
    if not (result := await result_dal.get_result_db(result_id)):
        message = f"Could not find result with ID {result_id}."
        raise HTTPException(status_code=404, detail=message)

    filename = result.filename if result.filename.endswith(".dcm") else result.filename + ".dcm"
    file_path = os.path.join(result.directory, filename)
    print("Loading dicom from: ", file_path)

    if not os.path.exists(file_path):
        message = f"Could not find DICOM file of result with ID: {result_id}."
        raise HTTPException(status_code=404, detail=message)

    return FileResponse(file_path, media_type="application/dicom")


app.include_router(exam_router, prefix="/api/v1/exam")
app.include_router(workflow_router, prefix="/api/v1/exam")
app.include_router(task_router, prefix="/api/v1/exam")
app.include_router(result_router, prefix="/api/v1/exam")
