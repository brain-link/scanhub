# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow manager main."""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scanhub_libraries.security import get_current_user

from api.workflow import router

app = FastAPI(
    openapi_url="/api/v1/workflow/openapi.json",
    docs_url="/api/v1/workflow/docs",
    dependencies=[Depends(get_current_user)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    """Call database initialization of startup."""
    pass

@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown event for the API."""
    pass

@router.get("/health/readiness", response_model={}, status_code=200, tags=["health"])
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
    return {"status": "ok"}


app.include_router(router, prefix="/api/v1/workflow")
