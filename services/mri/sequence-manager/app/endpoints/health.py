#!/usr/bin/env python3

# Project: ScanHub
# File: health.py
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
# Brief: Health check endpoint for FastAPI.

from fastapi import APIRouter, Depends, HTTPException, status
from database.mongodb import db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

async def check_db_connection() -> bool:
    """
    Check if the database connection is established.
    """
    logger.info(f"Checking database connection: db={db}, db.collection={db.collection}")
    if not db or not db.collection:
        return False
    return True

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(is_db_connected: bool = Depends(check_db_connection)):
    """
    Perform a health check for the microservice.

    Parameters:
    -----------
    is_db_connected: bool
        The status of the database connection.

    Returns:
    --------
    dict
        The status of the microservice.
    """
    logger.info(f"Database connection status: {is_db_connected}")
    if not is_db_connected:
        raise HTTPException(status_code=503, detail="Database not connected")
    return {"status": "OK"}

@router.get("/readiness", status_code=status.HTTP_200_OK)
async def readiness_check():
    """
    Perform a readiness check for the microservice.

    Returns:
    --------
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
