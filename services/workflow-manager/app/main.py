#!/usr/bin/env python3

# Project: ScanHub
# File: main.py
# Date: June 2023
#
# License:
# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
#
# SPDX-License-Identifier: GPL-3.0-only OR ScanHub commercial license
#
# Licensees holding valid ScanHub commercial licenses may use this file in
# accordance with the ScanHub Commercial License Agreement provided with the
# Software or, alternatively, in accordance with the GPL-3.0-only as published
# by the Free Software Foundation. Please refer to the License for the
# specific language governing the rights and limitations under either license.
#
# Brief: Workflow manager main.

from api.db import engine, init_db
from api.workflow import router
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect


app = FastAPI(
    openapi_url="/api/v1/workflow/openapi.json",
    docs_url="/api/v1/workflow/docs",
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

    Inspects sqlalchemy engine and check if workflow table exists.

    Returns
    -------
        Status docstring

    Raises
    ------
    HTTPException
        500: Workflow table does not exist
    """
    ins = inspect(engine)
    print(f"Found tables: {ins.get_table_names()}")
    if 'workflow' not in ins.get_table_names():
        raise HTTPException(status_code=500, detail="Could not find workflow table, table not created.")
    print("Healthcheck: Endpoint is ready.")
    return {'status': 'ok'}


app.include_router(router, prefix='/api/v1/workflow')
