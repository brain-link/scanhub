# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""MRI sequence manager main module."""

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.mongodb import close_mongo_connection, connect_to_mongo
from endpoints import health, mri_sequence_endpoints

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instantiate FastAPI app
app = FastAPI(
    openapi_url="/api/v1/mri/sequences/openapi.json",
    docs_url="/api/v1/mri/sequences/docs",
)

#   Wildcard ["*"] excludes eeverything that involves credentials
#   Better specify explicitly the allowed origins
#   See: https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    "http://localhost",
    "http://localhost:3000",  # frontned
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


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler.

    Parameters
    ----------
    request
        Request to be checked
    exc
        exception

    Returns
    -------
        Json response
    """
    logger.error("Request: %s %s\n%s", request.method, request.url, str(exc))
    return JSONResponse(status_code=500, content={"detail": str(exc)})


# Include routers for endpoints
app.include_router(
    mri_sequence_endpoints.router,
    prefix="/api/v1/mri/sequences",
    tags=["MRI Sequences"],
)
app.include_router(health.router)


@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup."""
    logger.info("StartUp...")
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown."""
    logger.info("ShutDown...")
    await close_mongo_connection()
