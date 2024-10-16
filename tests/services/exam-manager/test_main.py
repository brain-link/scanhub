# Copyright (C) 2024.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

""" pytest tests for main.py """

import http.client
import json

HOST = "localhost:8080"

class TestReadiness:
    """ Tests for endpoint /api/v1/exam/health/readiness """

    def test_readiness_A(self):
        connection = http.client.HTTPConnection(HOST, timeout=3)
        connection.request("GET", "/api/v1/exam/health/readiness")
        response = connection.getresponse()
        assert response.status == 200
        responsebody = response.read()
        responsebody_json = json.loads(responsebody)  # noqa: F841 (allow unused var)
        assert responsebody_json["status"] == "ok"

