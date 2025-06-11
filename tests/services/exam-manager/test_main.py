# Copyright (C) 2024.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

""" pytest tests for main.py """

import requests
import json

PREFIX = "https://localhost"


def test_readiness():
    response = requests.get(PREFIX + "/api/v1/exam/health/readiness", timeout=3, verify=False)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "ok"

