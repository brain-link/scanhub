# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Dependency file for FastAPI."""

from database.mongodb import Database, db
from fastapi import HTTPException, status


def get_database() -> Database:
    """Dependency for getting a handle to the MongoDB database."""
    if db is not None:
        return db
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database not connected",
    )
