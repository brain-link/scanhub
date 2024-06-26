# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Main file for the acquisition control service."""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scanhub_libraries.security import get_current_user

from api.acquisitioncontrol import router

app = FastAPI(
    openapi_url="/api/v1/mri/acquisitioncontrol/openapi.json",
    docs_url="/api/v1/mri/acquisitioncontrol/docs",
    dependencies=[Depends(get_current_user)]
)

# Wildcard ["*"] excludes eeverything that involves credentials
# Better specify explicitly the allowed origins
# See: https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    "http://localhost",
    "http://localhost:3000",  # frontend
    "http://localhost:8080",  # nginx
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@router.get("/health/readiness", response_model={}, status_code=200, tags=["health"])
async def readiness() -> dict:
    """Readiness health endpoint.

    Inspects service status.

    Returns
    -------
        Status docstring

    Raises
    ------
    HTTPException
        500: internal error
    """
    print("Healthcheck: Endpoint is ready.")
    return {"status": "ok"}


app.include_router(router, prefix="/api/v1/mri/acquisitioncontrol")
