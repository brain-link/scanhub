# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Configuration test."""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def test_client():
    """Create test client.

    Yields
    ------
        Test client
    """
    client = TestClient(app)
    yield client
