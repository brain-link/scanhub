# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Health check endpoint for FastAPI."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status

from database.mongodb import db

logger = logging.getLogger(__name__)

router = APIRouter()


async def check_db_connection() -> bool:
    """Check if the database connection is established."""
    logger.info(
        "Checking database connection: db=%s, db.collection=%s",
        str(db),
        str(db.collection),
    )
    return db.collection is not None



@router.get("/health", status_code=status.HTTP_200_OK, tags=["health"])
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
    return {"status": "OK"}


@router.get("/readiness", status_code=status.HTTP_200_OK, tags=["health"])
async def readiness_check():
    """Perform a readiness check for the microservice.

    Returns
    -------
    dict
        The readiness status of the microservice.
    """
    logger.info("Readiness check")
    return {"status": "ready"}


# from fastapi import APIRouter, Depends, HTTPException
# from app.database.mongodb import db
# import logging

# logger = logging.getLogger(__name__)

# router = APIRouter()

# async def check_db_connection() -> bool:
#     logger.info(f"Checking database connection: db={db}, db.collection={db.collection}")
#     if not db or not db.collection:
#         return False
#     return True

# @router.get("/health", status_code=200)
# async def health_check(is_db_connected: bool = Depends(check_db_connection)):
#     logger.info(f"Database connection status: {is_db_connected}")
#     if not is_db_connected:
#         raise HTTPException(status_code=503, detail="Database not connected")
#     return {"status": "OK"}
