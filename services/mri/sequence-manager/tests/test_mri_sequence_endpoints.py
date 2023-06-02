# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Test MRI sequence endpoints."""

from fastapi.testclient import TestClient
from main import app
from database.models import MRISequence

client = TestClient(app)

# Add test functions for create_sequence, get_sequences, update_sequence, delete_sequence, and search_sequences here