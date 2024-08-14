# Copyright (C) 2024.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

""" pytest tests for exam.py """

import http.client
import json

HOST = "localhost:8080"
CREDENTIALS_FROM_DATA = "grant_type=password&username=Max&password=letmein"


class TestPostNew:
    """ Tests for endpoint /api/v1/exam/new """

    def login(self):
        connection = http.client.HTTPConnection(HOST, timeout=3)
        connection.request("POST",
                           "/api/v1/userlogin/login",
                           CREDENTIALS_FROM_DATA,
                           {"Content-Type": "application/x-www-form-urlencoded"})
        response = connection.getresponse()
        assert response.status == 200
        responsebody = response.read()
        responsebody_json = json.loads(responsebody)
        return responsebody_json["access_token"]


    def test_post_new_A(self):
        # prepare
        access_token = self.login()

        # act
        exam = {
            "patient_id": 123,
            "name": "test_exam",
            "country": "blablastan",
            "site": "middle of nowhere",
            "address": "midway",
            "creator": "Max",
            "status": "NEW",
            "is_template": False,
            "is_frozen": False
        }
        connection = http.client.HTTPConnection(HOST, timeout=3)
        connection.request("POST", 
                           "/api/v1/exam/new",
                           json.dumps(exam),
                           {"Authorization": "Bearer " + access_token})
        response = connection.getresponse()
        
        # check
        assert response.status == 201
        responsebody = response.read()
        responsebody_json = json.loads(responsebody)  # noqa: F841 (allow unused var)
        for key in exam.keys():
            assert responsebody_json[key] == exam[key]

        # cleanup
        connection.request("DELETE", 
                           "/api/v1/exam/" + responsebody_json["id"],
                           json.dumps(exam),
                           {"Authorization": "Bearer " + access_token})


    def test_post_new_B(self):
        self.login()

        exam = {
            "patient_id": 123,
            "name": "test_exam",
            "country": "blablastan",
            "site": "middle of nowhere",
            "address": "midway",
            "creator": "Max",
            "status": "NEW",
            "is_template": False,
            "is_frozen": False
        }
        connection = http.client.HTTPConnection(HOST, timeout=3)
        connection.request("POST", 
                           "/api/v1/exam/new",
                           json.dumps(exam),
                           {"Authorization": "Bearer " + "somedummyaccesstoken"})
        response = connection.getresponse()

        assert response.status == 401


