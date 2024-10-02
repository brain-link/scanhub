# Copyright (C) 2024.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

""" pytest tests for exam.py """

import requests
# import sys
# sys.path.append("../../../services/exam-manager/app/")
# import dal


# TODO test if items are created/deleted/getted(!) recursively (exam->workflows->tasks)
# TODO test for create_exam_from_template if associated workflows/tasks are generated
# TODO make sure that template has no parent id and that instance has parent id
# TODO https://github.com/brain-link/scanhub/issues/133


HOST = "http://localhost:8080"
PREFIX = HOST + "/api/v1/exam"
PREFIX_PATIENT_MANAGER = HOST + "/api/v1/patient"
CREDENTIALS_FORM_DATA = "grant_type=password&username=Max&password=letmein"


def login():
    """ Get access token. """
    response = requests.post(
        "http://localhost:8080/api/v1/userlogin/login", 
        data=CREDENTIALS_FORM_DATA,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=3)
    assert response.status_code == 200
    response_json = response.json()
    return response_json["access_token"]


def test_invalid_and_no_token():
    login()
    request_list = [
        ["POST",    "/new"],
        ["POST",    "/"],
        ["GET",     "/123"],
        ["GET",     "/all/Meyer"],
        ["GET",     "/templates/all"],
        ["DELETE",  "/123"],
        ["PUT",     "/exampleExamId"],
        ["POST",    "/workflow/new"],
        ["POST",    "/workflow"],
        ["GET",     "/workflow/someWorkflowId"],
        ["GET",     "/workflow/all/someExamId"],
        ["GET",     "/workflow/templates/all"],
        ["DELETE",  "/workflow/someWorkflowId"],
        ["PUT",     "/workflow/someWorkflowId"],
        ["POST",    "/task/new"],
        ["POST",    "/task"],
        ["GET",     "/task/someTaskId"],
        ["GET",     "/task/all/someWorkflowId"],
        ["GET",     "/task/templates/all"],
        ["DELETE",  "/task/someTaskId"],
        ["put",     "/task/someTaskId"],
    ]
    def run_requests(headers, comment):
        for i, req in enumerate(request_list):
            response = requests.request(req[0], PREFIX + req[1], headers=headers)
            assert response.status_code == 401, \
                f"{comment}: request {i}: " + \
                "request not rejected with status_code 401."

    run_requests({"Authorization": "Bearer " + "wrongaccesstoken"}, "With wrong token")
    run_requests({}, "Without token")

    
def test_invalid_and_no_token_with_openapijson():
    openapijson_response = requests.get(PREFIX + "/openapi.json")
    assert openapijson_response.status_code == 200
    openapijson = openapijson_response.json()
    path_dict = openapijson["paths"]
    def run_requests(headers, comment):
        for path in path_dict:
            if path == "/api/v1/exam/health/readiness":
                continue
            for method in path_dict[path]:
                response = requests.request(
                    method.upper(), 
                    HOST + path, 
                    headers=headers)
                assert response.status_code == 401, \
                    f"{comment}: request {HOST}{path}:" + \
                    "request not rejected with status_code 401."
    run_requests({"Authorization": "Bearer " + "wrongaccesstoken"}, "With wrong token")
    run_requests({}, "Without token")


def test_create_exam():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    patient_1 = {
        "first_name": "Automated Test",
        "last_name": "Patient",
        "birth_date": "1977-07-17",
        "sex": "FEMALE",
        "issuer": "someone",
        "status": "NEW",
        "comment": None
    }
    postpatient_1_response = requests.post(
        PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers)
    assert postpatient_1_response.status_code == 201
    postpatient_1_response_json = postpatient_1_response.json()

    # act
    try:
        exam_1 = {
            "patient_id": postpatient_1_response_json["id"],
            "name": "test_exam",
            "country": "blablastan",
            "site": "middle of nowhere",
            "address": "midway",
            "status": "NEW",
            "is_template": False,
            "is_frozen": False
        }
        postexam_1_response = requests.post(
            PREFIX + "/new", json=exam_1, headers=headers)
        exam_2 = {
            "patient_id": postpatient_1_response_json["id"],
            "name": "test_exam",
            "country": "blablastan",
            "site": "middle of nowhere",
            "address": "midway",
            "status": "UPDATED",
            "is_template": False,
            "is_frozen": False
        }
        postexam_2_response = requests.post(
            PREFIX + "/new", json=exam_2, headers=headers)
        exam_3 = {
            "patient_id": 123,
            "name": "test_exam",
            "country": "blablastan",
            "site": "middle of nowhere",
            "address": "midway",
            "status": "NEW",
            "is_template": False,
            "is_frozen": False
        }
        postexam_3_response = requests.post(
            PREFIX + "/new", json=exam_3, headers=headers)

    # check
        assert postexam_1_response.status_code == 201
        postexam_1_response_json = postexam_1_response.json()
        for key in exam_1.keys():
            assert postexam_1_response_json[key] == exam_1[key]
        getexam_response = requests.get(
            PREFIX + "/" + postexam_1_response_json["id"],
            headers=headers)
        assert getexam_response.status_code == 200
        getexam_response_json = getexam_response.json()
        for key in exam_1.keys():
            assert getexam_response_json[key] == exam_1[key]
        assert postexam_2_response.status_code == 400, \
            'Status "UPDATED" should get rejected'
        assert postexam_3_response.status_code == 400, \
            "Wrong patient_id should get rejected."

    # cleanup
    finally:
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers)
            assert deletepatient_1_response.status_code == 204

        if postexam_1_response.status_code == 201:
            deleteexam_1_response = requests.delete(
                PREFIX + "/" + 
                postexam_1_response_json["id"],
                headers=headers)
            assert deleteexam_1_response.status_code == 204


def test_create_exam_from_template():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    exam_template = {
        "name": "test_exam_template",
        "country": "blablastan",
        "site": "middle of nowhere",
        "address": "midway",
        "status": "NEW",
        "is_template": True,
        "is_frozen": False
    }
    updated_template = {
        "name": "test_exam_template",
        "country": "blablastan",
        "site": "middle of nowhere",
        "address": "midway",
        "status": "UPDATED",
        "is_template": True,
        "is_frozen": False
    }
    patient_1 = {
        "first_name": "Automated Test",
        "last_name": "Patient",
        "birth_date": "1977-07-17",
        "sex": "FEMALE",
        "issuer": "someone",
        "status": "NEW",
        "comment": None
    }
    try:
        postnewtemplate_response = requests.post(
            PREFIX + "/new", json=exam_template, headers=headers)
        assert postnewtemplate_response.status_code == 201
        postnewtemplate_response_json = postnewtemplate_response.json()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam = {
            "patient_id": postpatient_1_response_json["id"],
            "name": "test_exam",
            "country": "blablastan",
            "site": "middle of nowhere",
            "address": "midway",
            "status": "NEW",
            "is_template": False,
            "is_frozen": False
        }
        postexam_response = requests.post(PREFIX + "/new", json=exam, headers=headers)
        assert postexam_response.status_code == 201
        postexam_response_json = postexam_response.json()

    # act
        postexamfromtemplate_1_response = requests.post(
            PREFIX + "/",
            params={
                "patient_id": postpatient_1_response_json["id"], 
                "template_id": postnewtemplate_response_json["id"],
                "new_exam_is_template": False
            },
            headers=headers)
        assert postexamfromtemplate_1_response.status_code == 201
        postexamfromtemplate_1_response_json = postexamfromtemplate_1_response.json()
        postexamfromtemplate_2_response = requests.post(
            PREFIX + "/",
            params={
                "patient_id": 123, 
                "template_id": postnewtemplate_response_json["id"],
                "new_exam_is_template": False
            },
            headers=headers)
        putupdatedtemplate_response = requests.put(
            PREFIX + "/" + postnewtemplate_response_json["id"],
            json=updated_template,
            headers=headers)
        assert putupdatedtemplate_response.status_code == 200
        putupdatedtemplate_response_json = putupdatedtemplate_response.json()
        postexamfromupdatedtemplate_response = requests.post(
            PREFIX + "/",
            params={
                "patient_id": postpatient_1_response_json["id"], 
                "template_id": putupdatedtemplate_response_json["id"],
                "new_exam_is_template": False
            },
            headers=headers)
        assert postexamfromupdatedtemplate_response.status_code == 201
        postexamfromupdatedtemplate_response_json = \
            postexamfromupdatedtemplate_response.json()
        postexamfrominstance_response = requests.post(
            PREFIX + "/",
            params={
                "patient_id": 333, 
                "template_id": postexam_response_json["id"],
                "new_exam_is_template": False
            },
            headers=headers)

    # check
        for key in exam_template.keys():
            if key != "is_template":
                assert postexamfromtemplate_1_response_json[key] == exam_template[key]
        assert postexamfromtemplate_1_response_json["patient_id"] == \
            postpatient_1_response_json["id"]
        assert postexamfromtemplate_1_response_json["is_template"] is False
        getexam_response = requests.get(
            PREFIX + "/" + postexamfromtemplate_1_response_json["id"],
            headers=headers)
        assert getexam_response.status_code == 200
        getexam_response_json = getexam_response.json()
        for key in exam_template.keys():
            if key != "is_template":
                assert getexam_response_json[key] == exam_template[key]
        assert getexam_response_json["patient_id"] == postpatient_1_response_json["id"]
        assert getexam_response_json["is_template"] is False
        assert postexamfromtemplate_2_response.status_code == 400, \
            "Create exam from template should reject invalid patient_id."
        assert postexamfromupdatedtemplate_response_json["status"] == "NEW", \
            "Status of new instance needs to be NEW, even if template has other status"
        assert postexamfrominstance_response.status_code == 400, \
            "Should only allow create from template, not from instance."

    # cleanup
    finally:
        if postnewtemplate_response.status_code == 201:
            deleteexamtemplate_response = requests.delete(
                PREFIX + "/" + postnewtemplate_response_json["id"],
                headers=headers)
            assert deleteexamtemplate_response.status_code == 204
        if postexamfromtemplate_1_response.status_code == 201:
            deleteexam_1_response = requests.delete(
                PREFIX + "/" + postexamfromtemplate_1_response_json["id"],
                headers=headers)
            assert deleteexam_1_response.status_code == 204
        if postexamfromupdatedtemplate_response.status_code == 201:
            deleteexam_2_response = requests.delete(
                PREFIX + "/" + postexamfromupdatedtemplate_response_json["id"],
                headers=headers)
            assert deleteexam_2_response.status_code == 204
        if postexam_response.status_code == 201:
            deleteexam_3_response = requests.delete(
                PREFIX + "/" + postexam_response_json["id"],
                headers=headers)
            assert deleteexam_3_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers)
            assert deletepatient_1_response.status_code == 204


def test_get_exam():
    # Successfully getting an exam is already tested in test_create_exam.
    access_token = login()
    getexam_response = requests.get(
        PREFIX + "/123",
        headers={"Authorization": "Bearer " + access_token})
    assert getexam_response.status_code == 500   # invalid uuid format
    getexam_response = requests.get(
        PREFIX + "/4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5",
        headers={"Authorization": "Bearer " + access_token})
    assert getexam_response.status_code == 404


def test_get_all_patient_exams():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = {
            "first_name": "Automated Test",
            "last_name": "Patient",
            "birth_date": "1977-07-17",
            "sex": "FEMALE",
            "issuer": "someone",
            "status": "NEW",
            "comment": None
        }
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        postpatient_1A_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers)
        assert postpatient_1A_response.status_code == 201
        postpatient_1A_response_json = postpatient_1A_response.json()
        exam1 = {
            "patient_id": postpatient_1_response_json["id"],
            "name": "test_exam",
            "country": "blablastan",
            "site": "middle of nowhere",
            "address": "midway",
            "status": "NEW",
            "is_template": False,
            "is_frozen": False
        }
        exam2 = exam1.copy()
        exam2["site"] = "test site 2"
        exam3 = exam1.copy()
        exam3["site"] = "test site 3"
        exam3["patient_id"] = postpatient_1A_response_json["id"]
        postnewexam1_response = requests.post(
            PREFIX + "/new", json=exam1, headers=headers)
        postnewexam2_response = requests.post(
            PREFIX + "/new", json=exam2, headers=headers)
        postnewexam3_response = requests.post(
            PREFIX + "/new", json=exam3, headers=headers)
        assert postnewexam1_response.status_code == 201
        assert postnewexam2_response.status_code == 201
        assert postnewexam3_response.status_code == 201

    # act
        getallexams_response = requests.get(
            PREFIX + "/all/" + str(postpatient_1_response_json["id"]), headers=headers)

    # check
        assert getallexams_response.status_code == 200
        getallexams_response_json = getallexams_response.json()
        assert len(getallexams_response_json) == 2

        def exam_in_response(exam):
            for exam_json_found in getallexams_response_json:
                exam_matches = True
                for key in exam.keys():
                    if exam[key] != exam_json_found[key]:
                        exam_matches = False
                if exam_matches:
                    return True
            return False

        assert exam_in_response(exam1)
        assert exam_in_response(exam2)
        assert not exam_in_response(exam3)

    # cleanup
    finally:
        if postnewexam1_response.status_code == 201:
            deleteexam1_response = requests.delete(
                PREFIX + "/" + postnewexam1_response.json()["id"], headers=headers)
            assert deleteexam1_response.status_code == 204
        if postnewexam2_response.status_code == 201:
            deleteexam2_response = requests.delete(
                PREFIX + "/" + postnewexam2_response.json()["id"], headers=headers)
            assert deleteexam2_response.status_code == 204
        if postnewexam3_response.status_code == 201:
            deleteexam3_response = requests.delete(
                PREFIX + "/" + postnewexam3_response.json()["id"], headers=headers)
            assert deleteexam3_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers)
            assert deletepatient_1_response.status_code == 204
        if postpatient_1A_response.status_code == 201:
            deletepatient_1A_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1A_response_json["id"]),
                headers=headers)
            assert deletepatient_1A_response.status_code == 204


def test_get_all_exam_templates():
    # prepare
    access_token = login()
    exam_template_1 = {
        "name": "test_exam_template",
        "country": "blablastan",
        "site": "middle of nowhere",
        "address": "midway",
        "status": "NEW",
        "is_template": True,
        "is_frozen": False
    }
    exam_template_2 = exam_template_1.copy()
    exam_template_2["site"] = "template 2 site"
    try:
        postnewtemplate_1_response = requests.post(
            PREFIX + "/new",
            json=exam_template_1,
            headers={"Authorization": "Bearer " + access_token})
        assert postnewtemplate_1_response.status_code == 201
        postnewtemplate_1_response_json = postnewtemplate_1_response.json()
        postnewtemplate_2_response = requests.post(
            PREFIX + "/new",
            json=exam_template_2,
            headers={"Authorization": "Bearer " + access_token})
        assert postnewtemplate_2_response.status_code == 201
        postnewtemplate_2_response_json = postnewtemplate_2_response.json()

    # act
        getalltemplates_response = requests.get(
            PREFIX + "/templates/all",
            headers={"Authorization": "Bearer " + access_token})

    # check
        assert getalltemplates_response.status_code == 200
        getalltemplates_response_json = getalltemplates_response.json()
        assert len(getalltemplates_response_json) >= 2
        
        def exam_template_in_received_list(exam_template):
            for exam_template_json_found in getalltemplates_response_json:
                assert exam_template_json_found["is_template"] is True
                exam_template_matches = True
                for key in exam_template.keys():
                    if exam_template[key] != exam_template_json_found[key]:
                        exam_template_matches = False
                if exam_template_matches:
                    return True
            return False

        assert exam_template_in_received_list(exam_template_1)
        assert exam_template_in_received_list(exam_template_2)

    # cleanup
    finally:
        if postnewtemplate_1_response.status_code == 201:
            deleteexamtemplate_1_presponse = requests.delete(
                PREFIX + "/" + postnewtemplate_1_response_json["id"],
                headers={"Authorization": "Bearer " + access_token},
            )
            assert deleteexamtemplate_1_presponse.status_code == 204
        if postnewtemplate_2_response.status_code == 201:
            deleteexamtemplate_2_presponse = requests.delete(
                PREFIX + "/" + postnewtemplate_2_response_json["id"],
                headers={"Authorization": "Bearer " + access_token},
            )
            assert deleteexamtemplate_2_presponse.status_code == 204


def test_exam_delete():
    # prepare / act
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = {
            "first_name": "Automated Test",
            "last_name": "Patient",
            "birth_date": "1977-07-17",
            "sex": "FEMALE",
            "issuer": "someone",
            "status": "NEW",
            "comment": None
        }
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam = {
            "patient_id": postpatient_1_response_json["id"],
            "name": "test_exam",
            "country": "blablastan",
            "site": "middle of nowhere",
            "address": "midway",
            "status": "NEW",
            "is_template": False,
            "is_frozen": False
        }
        postnewexam_response = requests.post(
            PREFIX + "/new", json=exam, headers=headers)
        assert postnewexam_response.status_code == 201
        postnewexam_response_json = postnewexam_response.json()
        deleteexam_response = requests.delete(
            PREFIX + "/" + postnewexam_response_json["id"],
            headers=headers
        )
        assert deleteexam_response.status_code == 204

        exam_template = {
            "name": "test_exam_template",
            "country": "blablastan",
            "site": "middle of nowhere",
            "address": "midway",
            "status": "NEW",
            "is_template": True,
            "is_frozen": False
        }
        postnewtemplate_response = requests.post(
            PREFIX + "/new", json=exam_template, headers=headers)
        assert postnewtemplate_response.status_code == 201
        postnewtemplate_response_json = postnewtemplate_response.json()
        deleteexamtemplate_presponse = requests.delete(
            PREFIX + "/" + postnewtemplate_response_json["id"],
            headers=headers,
        )
        assert deleteexamtemplate_presponse.status_code == 204

        # exam_frozen = exam.copy()
        # exam_frozen["is_frozen"] = True
        # postnewexamfrozen_response = requests.post(
        #     PREFIX + "/new",
        #     json=exam_frozen,
        #     headers={"Authorization": "Bearer " + access_token}
        # )
        # assert postnewexamfrozen_response.status_code == 201

    # check
        getexam_response = requests.get(
            PREFIX + "/" + postnewexam_response_json["id"],
            headers=headers)
        assert getexam_response.status_code == 404
        getexamtemplate_response = requests.get(
            PREFIX + "/" + postnewtemplate_response_json["id"],
            headers=headers)
        assert getexamtemplate_response.status_code == 404

        # postnewexamfrozen_response_json = postnewexamfrozen_response.json()
        # deleteexamfrozen_response = requests.delete(
        #     PREFIX + "/" + postnewexamfrozen_response_json["id"],
        #     headers={"Authorization": "Bearer " + access_token}
        # )
        # assert deleteexamfrozen_response.status_code == 404

    # cleanup
    # TODO implement cleanup of frozen item
    finally:
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers)
            assert deletepatient_1_response.status_code == 204


def test_update_exam():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = {
            "first_name": "Automated Test",
            "last_name": "Patient",
            "birth_date": "1977-07-17",
            "sex": "FEMALE",
            "issuer": "someone",
            "status": "NEW",
            "comment": None
        }
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        postpatient_1A_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers)
        assert postpatient_1A_response.status_code == 201
        postpatient_1A_response_json = postpatient_1A_response.json()
        exam = {
            "patient_id": postpatient_1_response_json["id"],
            "name": "test_exam",
            "country": "blablastan",
            "site": "middle of nowhere",
            "address": "midway",
            "status": "NEW",
            "is_template": False,
            "is_frozen": False
        }
        postexam_response = requests.post(PREFIX + "/new", json=exam, headers=headers)
        assert postexam_response.status_code == 201
        update_request_1 = {
            "patient_id": postpatient_1A_response_json["id"],
            "name": "updated_exam",
            "country": "updated country",
            "site": "updated site, still in the middle of nowhere",
            "address": "updated address midway",
            "status": "UPDATED",
            "is_template": False,
            "is_frozen": False,  # False, otherwise it can't be deleted after test
        }
        update_request_2 = update_request_1.copy()
        update_request_2["status"] = "NEW"
        update_request_3 = update_request_1.copy()
        update_request_3["patient_id"] = 333

    # act
        postexam_response_json = postexam_response.json()
        updateexam_response = requests.put(
            PREFIX + "/" + postexam_response_json["id"],
            json=update_request_1,
            headers=headers
        )

    # check
        assert updateexam_response.status_code == 200
        updateexam_response = updateexam_response.json()
        for key in update_request_1.keys():
            assert updateexam_response[key] == update_request_1[key]
        getexam_response = requests.get(
            PREFIX + "/" + postexam_response_json["id"],
            headers=headers)
        assert getexam_response.status_code == 200
        getexam_response_json = getexam_response.json()
        for key in update_request_1.keys():
            if key != "status":
                assert getexam_response_json[key] == update_request_1[key]

    # act
        updateexam_2_response = requests.put(
            PREFIX + "/" + postexam_response_json["id"], 
            json=update_request_2, 
            headers=headers
        )
    # check
        assert updateexam_2_response.status_code == 403, \
            "Update status to NEW should be rejected."

    # act
        updateexam_3_response = requests.put(
            PREFIX + "/" + postexam_response_json["id"], 
            json=update_request_3, 
            headers=headers
        )
    # check
        assert updateexam_3_response.status_code == 400, \
            "Wrong patient_id should be rejected."

    # cleanup
    finally:
        if postexam_response.status_code == 201:
            deleteexam_response = requests.delete(
                PREFIX + "/" + 
                postexam_response_json["id"],
                headers=headers)
            assert deleteexam_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers)
            assert deletepatient_1_response.status_code == 204
        if postpatient_1A_response.status_code == 201:
            deletepatient_1A_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1A_response_json["id"]),
                headers=headers)
            assert deletepatient_1A_response.status_code == 204


def test_create_workflow():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        workflow_1 = {
            "name": "test_workflow",
            "comment": "test comment",
            "exam_id": None,
            "is_finished": False,
            "is_template": False,
            "is_frozen": False
        }
        workflow_2 = workflow_1.copy()
        workflow_2["exam_id"] = "4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5"
        patient_1 = {
            "first_name": "Automated Test",
            "last_name": "Patient",
            "birth_date": "1977-07-17",
            "sex": "FEMALE",
            "issuer": "someone",
            "status": "NEW",
            "comment": None
        }
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam = {
            "patient_id": postpatient_1_response_json["id"],
            "name": "test_exam",
            "country": "blablastan",
            "site": "middle of nowhere",
            "address": "midway",
            "status": "NEW",
            "is_template": False,
            "is_frozen": False
        }
        exam_template = {
            "name": "test_exam_template",
            "country": "blablastan",
            "site": "middle of nowhere",
            "address": "midway",
            "status": "NEW",
            "is_template": True,
            "is_frozen": False
        }
        postexam_response = requests.post(PREFIX + "/new", json=exam, headers=headers)
        postexamtemplate_response = requests.post(
            PREFIX + "/new", json=exam_template, headers=headers)
        assert postexam_response.status_code == 201
        postexam_response_json = postexam_response.json()
        assert postexamtemplate_response.status_code == 201
        postexamtemplate_response_json = postexamtemplate_response.json()
        workflow_3 = workflow_1.copy()
        workflow_3["exam_id"] = postexam_response_json["id"]
        workflow_4 = workflow_1.copy()
        workflow_4["exam_id"] = postexam_response_json["id"]
        workflow_4["is_template"] = True
        workflow_5 = workflow_1.copy()
        workflow_5["exam_id"] = postexamtemplate_response_json["id"]

    # act
        postworkflow_response_1 = requests.post(
            PREFIX + "/workflow/new", json=workflow_1, headers=headers)
        postworkflow_response_2 = requests.post(
            PREFIX + "/workflow/new", json=workflow_2, headers=headers)
        postworkflow_response_3 = requests.post(
            PREFIX + "/workflow/new", json=workflow_3, headers=headers)
        postworkflow_response_4 = requests.post(
            PREFIX + "/workflow/new", json=workflow_4, headers=headers)
        postworkflow_response_5 = requests.post(
            PREFIX + "/workflow/new", json=workflow_5, headers=headers)

    # check
        assert postworkflow_response_1.status_code == 400, \
            "Workflow instance without exam_id should be rejected."
        assert postworkflow_response_2.status_code == 400, \
            "Workflow with wrong exam_id should be rejected."
        assert postworkflow_response_3.status_code == 201
        assert postworkflow_response_4.status_code == 400, \
            "Workflow template that refers to exam instance should be rejected."
        assert postworkflow_response_5.status_code == 400, \
            "Workflow instance that refers to template should be rejected."
        # TODO check the same for the API calls that update exams, workflows, tasks
        postworkflow_response_json_3 = postworkflow_response_3.json()
        for key in workflow_3.keys():
            assert postworkflow_response_json_3[key] == workflow_3[key]
        getworkflow_response = requests.get(
            PREFIX + "/workflow/" + postworkflow_response_json_3["id"],
            headers=headers)
        assert getworkflow_response.status_code == 200
        getworkflow_response_json = getworkflow_response.json()
        for key in workflow_3.keys():
            assert getworkflow_response_json[key] == workflow_3[key]

    # cleanup
    finally:
        if postexam_response.status_code == 201:
            deleteexam_response = requests.delete(
                PREFIX + "/" + postexam_response_json["id"], headers=headers)
            assert deleteexam_response.status_code == 204
        if postexamtemplate_response.status_code == 201:
            postexamtemplate_response_json = postexamtemplate_response.json()
            deleteexamtemplate_response = requests.delete(
                PREFIX + "/" + postexamtemplate_response_json["id"], headers=headers)
            assert deleteexamtemplate_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers)
            assert deletepatient_1_response.status_code == 204
        # deleting an exam, recursively deletes the corresponding workflows


def test_create_workflow_from_template():
    # TODO work in progress
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = {
            "first_name": "Automated Test",
            "last_name": "Patient",
            "birth_date": "1977-07-17",
            "sex": "FEMALE",
            "issuer": "someone",
            "status": "NEW",
            "comment": None
        }
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        workflow_template = {
            "name": "test_workflow_template",
            "comment": "test comment",
            "is_finished": False,
            "is_template": True,
            "is_frozen": False
        }
        exam = {
            "patient_id": postpatient_1_response_json["id"],
            "name": "test_exam",
            "country": "blablastan",
            "site": "middle of nowhere",
            "address": "midway",
            "status": "NEW",
            "is_template": False,
            "is_frozen": False
        }
        postexam_response = requests.post(PREFIX + "/new", json=exam, headers=headers)
        assert postexam_response.status_code == 201
        postexam_response_json = postexam_response.json()
        postnewtemplate_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template, headers=headers)
        assert postnewtemplate_response.status_code == 201
        postnewtemplate_response_json = postnewtemplate_response.json()
        workflow = {
            "exam_id": postexam_response_json["id"],
            "name": "test_workflow_template",
            "comment": "test comment",
            "is_finished": False,
            "is_template": False,
            "is_frozen": False
        }
        postworkflow_response = requests.post(
            PREFIX + "/workflow/new", json=workflow, headers=headers)
        assert postworkflow_response.status_code == 201
        postworkflow_response_json = postworkflow_response.json()

    # act
        postworkflowfromtemplate_response = requests.post(
            PREFIX + "/workflow",
            params={
                "exam_id": postexam_response_json["id"], 
                "template_id": postnewtemplate_response_json["id"],
                "new_workflow_is_template": False   # could also check with True
            },
            headers=headers)
        postworkflowfromtemplate_fail_1_response = requests.post(
            PREFIX + "/workflow",
            params={
                "exam_id": postexam_response_json["id"], 
                "template_id": postworkflow_response_json["id"],
                "new_workflow_is_template": False   # could also check with True
            },
            headers=headers)

    # check
        assert postworkflowfromtemplate_response.status_code == 201
        postworkflowfromtemplate_response_json = \
            postworkflowfromtemplate_response.json()
        for key in workflow_template.keys():
            if key != "is_template":
                assert postworkflowfromtemplate_response_json[key] == \
                    workflow_template[key]
        assert postworkflowfromtemplate_response_json["exam_id"] == \
            postexam_response_json["id"]
        assert postworkflowfromtemplate_response_json["is_template"] is False
        getworkflow_response = requests.get(
            PREFIX + "/workflow/" + postworkflowfromtemplate_response_json["id"], 
            headers=headers)
        assert getworkflow_response.status_code == 200
        getworkflow_response_json = getworkflow_response.json()
        for key in workflow_template.keys():
            if key != "is_template":
                assert getworkflow_response_json[key] == workflow_template[key]
        assert getworkflow_response_json["exam_id"] == \
            postexam_response_json["id"]
        assert getworkflow_response_json["is_template"] is False
        assert postworkflowfromtemplate_fail_1_response.status_code == 400

    # cleanup
    finally:
        # deleting exam recursively deletes associated workflows
        deleteexam_response = requests.delete(
            PREFIX + "/" + postexam_response_json["id"], headers=headers)
        assert deleteexam_response.status_code == 204
        if postnewtemplate_response.status_code == 201:
            deleteworkflowtemplate_response = requests.delete(
                PREFIX + "/workflow/" + postnewtemplate_response_json["id"], 
                headers=headers)
            assert deleteworkflowtemplate_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers)
            assert deletepatient_1_response.status_code == 204
