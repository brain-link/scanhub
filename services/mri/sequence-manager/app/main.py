# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""MRI sequence manager main module."""

import logging

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.mongodb import close_mongo_connection, connect_to_mongo, db
from endpoints import mri_sequence_endpoints

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
    "http://localhost",       # frontend via nginx-proxy
    "https://localhost",      # frontend via nginx-proxy
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


async def check_db_connection() -> bool:
    """Check if the database connection is established."""
    logger.info(
        "Checking database connection: db=%s, db.collection=%s",
        str(db),
        str(db.collection),
    )
    return db.collection is not None


@app.get("/api/v1/mri/sequences/health", status_code=status.HTTP_200_OK, tags=["health"])
async def health_check(
    is_db_connected: bool = Depends(check_db_connection),
) -> dict[str, str]:
    """
    Perform a health check for the microservice.

    Parameters
    ----------
    is_db_connected: bool
        The status of the database connection.

    Returns
    -------
        The status of the microservice.
    """
    logger.info("Database connection status: %r", is_db_connected)
    if not is_db_connected:
        raise HTTPException(status_code=503, detail="Database not connected")
    return {"status": "ok"}


# Include routers for endpoints
app.include_router(
    mri_sequence_endpoints.router,
    prefix="/api/v1/mri/sequences",
    tags=["MRI Sequences"],
)
