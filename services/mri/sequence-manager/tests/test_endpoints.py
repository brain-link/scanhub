# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Test endpoints."""

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_check():
    """Check if healthy."""
    response = client.get("/health")
    assert response.status_code == 200  # noqa: S101
    assert response.json() == {"status": "OK"}  # noqa: S101

def test_readiness_check():
    """Check if ready."""
    response = client.get("/readiness")
    assert response.status_code == 200  # noqa: S101
    assert response.json() == {"status": "ready"}   # noqa: S101

# Add more test functions for other endpoints here
