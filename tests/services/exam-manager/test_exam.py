# Copyright (C) 2024.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

""" pytest tests for exam.py """

import requests
import json
# import sys
# sys.path.append("../../../services/exam-manager/app/")
# import dal

# TODO implement tests for status DELETED


HOST = "https://localhost"
PREFIX = HOST + "/api/v1/exam"
PREFIX_PATIENT_MANAGER = HOST + "/api/v1/patient"
USERNAME = "Max"            #   make sure this user is installed with this password
PASSWORD = "maxmaxmaxmax"   #   they are not set up by this test routine
CREDENTIALS_FORM_DATA = "grant_type=password&username=" + USERNAME + "&password=" + PASSWORD


PATIENT = {
    "first_name": "Automated Test",
    "last_name": "Patient",
    "birth_date": "1977-07-17",
    "sex": "FEMALE",
    "issuer": "someone",
    "status": "NEW",
    "comment": None
}

EXAM_TEMPLATE = {
#    "patient_id": None,
    "name": "Automated test exam",
    "description": "Some test description",
    "indication": "Some test indication",
    "patient_height_cm": 150,
    "patient_weight_kg": 50,
    "comment": "Some test comment",
    "status": "NEW",
    "is_template": True,
}

WORKFLOW_TEMPLATE = {
#    "exam_id": None,
    "name": "Automated test workflow",
    "description": "test description",
    "comment": "test comment",
    "status": "NEW",
    "is_template": True,
}

TASK_TEMPLATE = {
#    "workflow_id": None,
    "name": "Automated test task",
    "description": "some test task description",
    "comment": "some test comment",
    "type": "PROCESSING_TASK",
    "args": {
        "arg1": "val1",
        "arg2": "val2",
        "arg3": "val3"
    },
    "artifacts": {
        "some unspecified artifacts": "yay",
        # could enforce form of the values for input and output in the future
        "input": json.dumps([
            {
                "path": "/data",
                "name": "inputfile2"
            }
        ]),
        "output": json.dumps([
            {
                "path": "/data",
                "name": "outputfile1"
            }
        ])
    },
    "destinations": {
        "DICOM FANTASIA": "FANTASY PACS 1",
        "RAWDATA FANTASIA": "FANTASY EXPORT INTERFACE 1"
    },
    "status": "NEW",
    "progress": 50,
    "is_template": True,
}


def login():
    """ Get access token. """
    response = requests.post(
        HOST + "/api/v1/userlogin/login", 
        data=CREDENTIALS_FORM_DATA,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=3,
        verify=False)
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
            response = requests.request(req[0], PREFIX + req[1], headers=headers, verify=False)
            assert response.status_code == 401, \
                f"{comment}: request {i}: " + \
                "request not rejected with status_code 401."

    run_requests({"Authorization": "Bearer " + "wrongaccesstoken"}, "With wrong token")
    run_requests({}, "Without token")

    
def test_invalid_and_no_token_with_openapijson():
    openapijson_response = requests.get(PREFIX + "/openapi.json", verify=False)
    assert openapijson_response.status_code == 200
    openapijson = openapijson_response.json()
    path_dict = openapijson["paths"]
    def run_requests(headers, comment):
        for path in path_dict:
            if path == "/api/v1/exam/health/readiness":
                continue
            if path.count("{") == 1 and path.count("}") == 1 and path.endswith("}"):
                path_for_request = path[0:path.find("{")] + "c7b7c2ba-e6ca-4354-a1e9-697478565148"
            else:
                path_for_request = path
            for method in path_dict[path]:
                response = requests.request(
                    method.upper(), 
                    HOST + path_for_request, 
                    headers=headers,
                    verify=False)
                assert response.status_code == 401, \
                    f"{comment}: request {HOST}{path_for_request}:" + \
                    "request not rejected with status_code 401."
    run_requests({"Authorization": "Bearer " + "wrongaccesstoken"}, "With wrong token")
    run_requests({}, "Without token")


def test_create_exam():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    patient_1 = PATIENT.copy()
    postpatient_1_response = requests.post(
        PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
    assert postpatient_1_response.status_code == 201
    postpatient_1_response_json = postpatient_1_response.json()

    # act
    try:
        exam_1 = EXAM_TEMPLATE.copy()
        exam_1["is_template"] = False
        exam_1["patient_id"] = postpatient_1_response_json["id"]
        postexam_1_response = requests.post(
            PREFIX + "/new", json=exam_1, headers=headers, verify=False)
        exam_2 = EXAM_TEMPLATE.copy()
        exam_2["patient_id"] = postpatient_1_response_json["id"]
        exam_2["status"] = "UPDATED"
        exam_2["is_template"] = False
        postexam_2_response = requests.post(
            PREFIX + "/new", json=exam_2, headers=headers, verify=False)
        exam_3 = EXAM_TEMPLATE.copy()
        exam_3["patient_id"] = "4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5"
        exam_3["is_template"] = False
        postexam_3_response = requests.post(
            PREFIX + "/new", json=exam_3, headers=headers, verify=False)

    # check
        assert postexam_1_response.status_code == 201
        postexam_1_response_json = postexam_1_response.json()
        for key in exam_1.keys():
            assert postexam_1_response_json[key] == exam_1[key]
        getexam_response = requests.get(
            PREFIX + "/" + postexam_1_response_json["id"],
            headers=headers,
            verify=False)
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
                headers=headers,
                verify=False)
            assert deletepatient_1_response.status_code == 204

        if postexam_1_response.status_code == 201:
            deleteexam_1_response = requests.delete(
                PREFIX + "/" + 
                postexam_1_response_json["id"],
                headers=headers,
                verify=False)
            assert deleteexam_1_response.status_code == 204


def test_create_exam_from_template():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    exam_template = EXAM_TEMPLATE.copy()
    updated_template = EXAM_TEMPLATE.copy()
    updated_template["status"] = "UPDATED"
    patient_1 = PATIENT.copy()
    try:
        postnewtemplate_response = requests.post(
            PREFIX + "/new", json=exam_template, headers=headers, verify=False)
        assert postnewtemplate_response.status_code == 201
        postnewtemplate_response_json = postnewtemplate_response.json()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam = EXAM_TEMPLATE.copy()
        exam["patient_id"] = postpatient_1_response_json["id"]
        exam["is_template"] = False
        postexam_response = requests.post(PREFIX + "/new", json=exam, headers=headers, verify=False)
        assert postexam_response.status_code == 201
        postexam_response_json = postexam_response.json()
        exam_template_2 = EXAM_TEMPLATE.copy()
        exam_template_2["name"] = "Automated test exam template 2"
        postexamtemplate_2_response = requests.post(
            PREFIX + "/new", json=exam_template_2, headers=headers, verify=False)
        assert postexamtemplate_2_response.status_code == 201
        postexamtemplate_2_response_json = postexamtemplate_2_response.json()
        workflow_template_1 = WORKFLOW_TEMPLATE.copy()
        workflow_template_1["exam_id"] = postexamtemplate_2_response_json["id"]
        workflow_template_1["name"] = "Automated test workflow template 1"
        workflow_template_1["comment"] = "Belongs to 'automated test exam template 2'."
        workflow_template_2 = workflow_template_1.copy()
        workflow_template_2["name"] = "Automated test workflow template 2"
        workflow_template_2["comment"] = "Belongs to 'automated test exam template 2'."
        postworkflowtemplate_1_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template_1, headers=headers, verify=False)
        assert postworkflowtemplate_1_response.status_code == 201
        postworkflowtemplate_1_response_json = postworkflowtemplate_1_response.json()
        postworkflowtemplate_2_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template_2, headers=headers, verify=False)
        assert postworkflowtemplate_2_response.status_code == 201
        postworkflowtemplate_2_response_json = postworkflowtemplate_2_response.json()
        task_template_1 = TASK_TEMPLATE.copy()
        task_template_1["workflow_id"] = postworkflowtemplate_1_response_json["id"]
        task_template_2 = task_template_1.copy()
        task_template_2["name"] = "Automated test task template 2"
        task_template_3 = task_template_1.copy()
        task_template_3["name"] = "Automated test task template 3"
        task_template_3["workflow_id"] = postworkflowtemplate_2_response_json["id"]
        task_template_4 = task_template_1.copy()
        task_template_4["name"] = "Automated test task template 4"
        task_template_4["workflow_id"] = postworkflowtemplate_2_response_json["id"]
        posttasktemplate_2_response = requests.post(
            PREFIX + "/task/new", json=task_template_1, headers=headers, verify=False)
        assert posttasktemplate_2_response.status_code == 201
        posttasktemplate_2_response = requests.post(
            PREFIX + "/task/new", json=task_template_2, headers=headers, verify=False)
        assert posttasktemplate_2_response.status_code == 201
        posttasktemplate_2_response = requests.post(
            PREFIX + "/task/new", json=task_template_3, headers=headers, verify=False)
        assert posttasktemplate_2_response.status_code == 201
        posttasktemplate_2_response = requests.post(
            PREFIX + "/task/new", json=task_template_4, headers=headers, verify=False)
        assert posttasktemplate_2_response.status_code == 201

    # act
        examfromtemplate_1_request = postnewtemplate_response_json.copy()
        examfromtemplate_1_request["patient_id"] = postpatient_1_response_json["id"]
        examfromtemplate_1_request["is_template"] = False
        postexamfromtemplate_1_response = requests.post(
            PREFIX + "/",
            json=examfromtemplate_1_request,
            params={"template_id": postnewtemplate_response_json["id"]},
            headers=headers,
            verify=False)
        assert postexamfromtemplate_1_response.status_code == 201
        postexamfromtemplate_1_response_json = postexamfromtemplate_1_response.json()
        examfromtemplate_2_request = postnewtemplate_response_json.copy()
        examfromtemplate_2_request["patient_id"] = \
            "4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5"
        examfromtemplate_2_request["is_template"] = False
        postexamfromtemplate_2_response = requests.post(
            PREFIX + "/",
            json=examfromtemplate_2_request,
            params={"template_id": postnewtemplate_response_json["id"]},
            headers=headers,
            verify=False)
        putupdatedtemplate_response = requests.put(
            PREFIX + "/" + postnewtemplate_response_json["id"],
            json=updated_template,
            headers=headers,
            verify=False)
        assert putupdatedtemplate_response.status_code == 200
        putupdatedtemplate_response_json = putupdatedtemplate_response.json()
        examfromupdatedtemplate_request = putupdatedtemplate_response_json.copy()
        examfromupdatedtemplate_request["patient_id"] = \
            postpatient_1_response_json["id"]
        examfromupdatedtemplate_request["is_template"] = False
        postexamfromupdatedtemplate_response = requests.post(
            PREFIX + "/",
            json=examfromupdatedtemplate_request,
            params={"template_id": putupdatedtemplate_response_json["id"]},
            headers=headers,
            verify=False)
        assert postexamfromupdatedtemplate_response.status_code == 201
        postexamfromupdatedtemplate_response_json = \
            postexamfromupdatedtemplate_response.json()
        examfrominstance_request = postexam_response_json.copy()
        examfrominstance_request["patient_id"] = postexam_response_json["patient_id"]
        examfrominstance_request["is_template"] = False
        postexamfrominstance_response = requests.post(
            PREFIX + "/",
            json=examfrominstance_request,
            params={"template_id": postexam_response_json["id"]},
            headers=headers,
            verify=False)
        examfromtemplate_3_request = postexamtemplate_2_response_json.copy()
        examfromtemplate_3_request["patient_id"] = postpatient_1_response_json["id"]
        examfromtemplate_3_request["is_template"] = False
        postexamfromtemplate_3_response = requests.post(
            PREFIX + "/",
            json=examfromtemplate_3_request,
            params={"template_id": postexamtemplate_2_response_json["id"]},
            headers=headers,
            verify=False)
        assert postexamfromtemplate_3_response.status_code == 201
        postexamfromtemplate_3_response_json = postexamfromtemplate_3_response.json()

    # check
        for key in exam_template.keys():
            if key != "is_template":
                assert postexamfromtemplate_1_response_json[key] == exam_template[key]
        assert postexamfromtemplate_1_response_json["patient_id"] == \
            postpatient_1_response_json["id"]
        assert postexamfromtemplate_1_response_json["is_template"] is False
        getexam_response = requests.get(
            PREFIX + "/" + postexamfromtemplate_1_response_json["id"],
            headers=headers,
            verify=False)
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
        for key in exam_template_2.keys():
            if key != "is_template":
                assert postexamfromtemplate_3_response_json[key] == exam_template_2[key]
        assert postexamfromtemplate_3_response_json["is_template"] is False
        assert postexamfromtemplate_3_response_json["patient_id"] == \
            postpatient_1_response_json["id"]
        assert len(postexamfromtemplate_3_response_json["workflows"]) == 2
        def template_matches_itemlist(template, itemlist):
            for i, item_json_found in enumerate(itemlist):
                item_matches = True
                for key in template.keys():
                    if template[key] != item_json_found[key] \
                            and key != "is_template" \
                            and key != "exam_id" \
                            and key != "workflow_id":
                        item_matches = False
                if item_matches:
                    return i
            return -1
        wf1_index = template_matches_itemlist(
            workflow_template_1,
            postexamfromtemplate_3_response_json["workflows"]
        )
        wf2_index = template_matches_itemlist(
            workflow_template_2,
            postexamfromtemplate_3_response_json["workflows"]
        )
        assert wf1_index >= 0, "Workflow missing in response of create from template"
        assert wf2_index >= 0, "Workflow missing in response of create from template"
        t1_index = template_matches_itemlist(
            task_template_1,
            postexamfromtemplate_3_response_json["workflows"][wf1_index]["tasks"]
        )
        t2_index = template_matches_itemlist(
            task_template_2,
            postexamfromtemplate_3_response_json["workflows"][wf1_index]["tasks"]
        )
        t3_index = template_matches_itemlist(
            task_template_3,
            postexamfromtemplate_3_response_json["workflows"][wf2_index]["tasks"]
        )
        t4_index = template_matches_itemlist(
            task_template_4,
            postexamfromtemplate_3_response_json["workflows"][wf2_index]["tasks"]
        )
        assert t1_index >= 0, "Task missing in response of create from template"
        assert t2_index >= 0, "Task missing in response of create from template"
        assert t3_index >= 0, "Task missing in response of create from template"
        assert t4_index >= 0, "Task missing in response of create from template"
        getexam_3_response = requests.get(
            PREFIX + "/" + postexamfromtemplate_3_response_json["id"],
            headers=headers,
            verify=False)
        assert getexam_3_response.status_code == 200
        getexam_3_response_json = getexam_3_response.json()
        for key in exam_template_2.keys():
            if key != "is_template":
                assert getexam_3_response_json[key] == exam_template_2[key]
        assert getexam_3_response_json["is_template"] is False
        assert getexam_3_response_json["patient_id"] == \
            postpatient_1_response_json["id"]
        assert len(getexam_3_response_json["workflows"]) == 2
        wf1_index = template_matches_itemlist(
            workflow_template_1,
            getexam_3_response_json["workflows"]
        )
        wf2_index = template_matches_itemlist(
            workflow_template_2,
            getexam_3_response_json["workflows"]
        )
        assert wf1_index >= 0, "Workflow missing in response of get exam"
        assert wf2_index >= 0, "Workflow missing in response of get exam"
        t1_index = template_matches_itemlist(
            task_template_1,
            getexam_3_response_json["workflows"][wf1_index]["tasks"]
        )
        t2_index = template_matches_itemlist(
            task_template_2,
            getexam_3_response_json["workflows"][wf1_index]["tasks"]
        )
        t3_index = template_matches_itemlist(
            task_template_3,
            getexam_3_response_json["workflows"][wf2_index]["tasks"]
        )
        t4_index = template_matches_itemlist(
            task_template_4,
            getexam_3_response_json["workflows"][wf2_index]["tasks"]
        )
        assert t1_index >= 0, "Task missing in response of get exam"
        assert t2_index >= 0, "Task missing in response of get exam"
        assert t3_index >= 0, "Task missing in response of get exam"
        assert t4_index >= 0, "Task missing in response of get exam"

    # cleanup
    finally:
        if postnewtemplate_response.status_code == 201:
            deleteexamtemplate_response = requests.delete(
                PREFIX + "/" + postnewtemplate_response_json["id"],
                headers=headers,
                verify=False)
            assert deleteexamtemplate_response.status_code == 204
        if postexamfromtemplate_1_response.status_code == 201:
            deleteexam_1_response = requests.delete(
                PREFIX + "/" + postexamfromtemplate_1_response_json["id"],
                headers=headers,
                verify=False)
            assert deleteexam_1_response.status_code == 204
        if postexamfromupdatedtemplate_response.status_code == 201:
            deleteexam_2_response = requests.delete(
                PREFIX + "/" + postexamfromupdatedtemplate_response_json["id"],
                headers=headers,
                verify=False)
            assert deleteexam_2_response.status_code == 204
        if postexam_response.status_code == 201:
            deleteexam_3_response = requests.delete(
                PREFIX + "/" + postexam_response_json["id"],
                headers=headers,
                verify=False)
            assert deleteexam_3_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers,
                verify=False)
            assert deletepatient_1_response.status_code == 204
        if postexamtemplate_2_response.status_code == 201:
            deleteexamtemplate_2_response = requests.delete(
                PREFIX + "/" + postexamtemplate_2_response_json["id"],
                headers=headers,
                verify=False)
            assert deleteexamtemplate_2_response.status_code == 204
        if postexamfromtemplate_3_response.status_code == 201:
            deleteexamfromtemplate_3_response = requests.delete(
                PREFIX + "/" + postexamfromtemplate_3_response_json["id"],
                headers=headers,
                verify=False)
            assert deleteexamfromtemplate_3_response.status_code == 204


def test_get_exam():
    # Successfully getting an exam is already tested in test_create_exam.
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    getexam_response = requests.get(PREFIX + "/123", headers=headers, verify=False)
    assert getexam_response.status_code == 400   # invalid uuid format
    getexam_response = requests.get(
        PREFIX + "/4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5", headers=headers, verify=False)
    assert getexam_response.status_code == 404


def test_get_all_patient_exams():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        postpatient_1A_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1A_response.status_code == 201
        postpatient_1A_response_json = postpatient_1A_response.json()
        exam1 = EXAM_TEMPLATE.copy()
        exam1["patient_id"] = postpatient_1_response_json["id"]
        exam1["is_template"] = False
        exam2 = exam1.copy()
        exam2["description"] = "test description 2"
        exam3 = exam1.copy()
        exam3["description"] = "test description 3"
        exam3["patient_id"] = postpatient_1A_response_json["id"]
        postnewexam1_response = requests.post(
            PREFIX + "/new", json=exam1, headers=headers, verify=False)
        postnewexam2_response = requests.post(
            PREFIX + "/new", json=exam2, headers=headers, verify=False)
        postnewexam3_response = requests.post(
            PREFIX + "/new", json=exam3, headers=headers, verify=False)
        assert postnewexam1_response.status_code == 201
        assert postnewexam2_response.status_code == 201
        assert postnewexam3_response.status_code == 201

    # act
        getallexams_response = requests.get(
            PREFIX + "/all/" + str(postpatient_1_response_json["id"]), headers=headers, verify=False)

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
                PREFIX + "/" + postnewexam1_response.json()["id"], headers=headers, verify=False)
            assert deleteexam1_response.status_code == 204
        if postnewexam2_response.status_code == 201:
            deleteexam2_response = requests.delete(
                PREFIX + "/" + postnewexam2_response.json()["id"], headers=headers, verify=False)
            assert deleteexam2_response.status_code == 204
        if postnewexam3_response.status_code == 201:
            deleteexam3_response = requests.delete(
                PREFIX + "/" + postnewexam3_response.json()["id"], headers=headers, verify=False)
            assert deleteexam3_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers,
                verify=False)
            assert deletepatient_1_response.status_code == 204
        if postpatient_1A_response.status_code == 201:
            deletepatient_1A_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1A_response_json["id"]),
                headers=headers,
                verify=False)
            assert deletepatient_1A_response.status_code == 204


def test_get_all_exam_templates():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    exam_template_1 = EXAM_TEMPLATE.copy()
    exam_template_2 = exam_template_1.copy()
    exam_template_2["description"] = "description 2"
    try:
        getalltemplatesbefore_response = requests.get(
            PREFIX + "/templates/all", headers=headers, verify=False)
        assert getalltemplatesbefore_response.status_code == 200
        getalltemplatesbefore_response_json = getalltemplatesbefore_response.json()
        postnewtemplate_1_response = requests.post(
            PREFIX + "/new", json=exam_template_1, headers=headers, verify=False)
        assert postnewtemplate_1_response.status_code == 201
        postnewtemplate_1_response_json = postnewtemplate_1_response.json()
        postnewtemplate_2_response = requests.post(
            PREFIX + "/new", json=exam_template_2, headers=headers, verify=False)
        assert postnewtemplate_2_response.status_code == 201
        postnewtemplate_2_response_json = postnewtemplate_2_response.json()

    # act
        getalltemplates_response = requests.get(
            PREFIX + "/templates/all", headers=headers, verify=False)

    # check
        assert getalltemplates_response.status_code == 200
        getalltemplates_response_json = getalltemplates_response.json()
        assert len(getalltemplates_response_json) \
            - len(getalltemplatesbefore_response_json) == 2
        
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
                PREFIX + "/" + postnewtemplate_1_response_json["id"], headers=headers, verify=False)
            assert deleteexamtemplate_1_presponse.status_code == 204
        if postnewtemplate_2_response.status_code == 201:
            deleteexamtemplate_2_presponse = requests.delete(
                PREFIX + "/" + postnewtemplate_2_response_json["id"], headers=headers, verify=False)
            assert deleteexamtemplate_2_presponse.status_code == 204


def test_delete_exam():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam = EXAM_TEMPLATE.copy()
        exam["patient_id"] = postpatient_1_response_json["id"]
        exam["is_template"] = False
        postnewexam_response = requests.post(
            PREFIX + "/new", json=exam, headers=headers, verify=False)
        assert postnewexam_response.status_code == 201
        postnewexam_response_json = postnewexam_response.json()
        exam_2 = exam.copy()
        exam_2["name"] = "Automated test exam 2"
        postnewexam_2_response = requests.post(
            PREFIX + "/new", json=exam_2, headers=headers, verify=False)
        assert postnewexam_2_response.status_code == 201
        postnewexam_2_response_json = postnewexam_2_response.json()
        exam_template = EXAM_TEMPLATE.copy()
        postnewtemplate_response = requests.post(
            PREFIX + "/new", json=exam_template, headers=headers, verify=False)
        assert postnewtemplate_response.status_code == 201
        postnewtemplate_response_json = postnewtemplate_response.json()

        # act
        deleteexam_response = requests.delete(
            PREFIX + "/" + postnewexam_response_json["id"],
            headers=headers,
            verify=False
        )
        assert deleteexam_response.status_code == 204
        deleteexamtemplate_presponse = requests.delete(
            PREFIX + "/" + postnewtemplate_response_json["id"],
            headers=headers,
            verify=False
        )
        assert deleteexamtemplate_presponse.status_code == 204

    # check
        getexam_response = requests.get(
            PREFIX + "/" + postnewexam_response_json["id"],
            headers=headers,
            verify=False
        )
        assert getexam_response.status_code == 404
        getexam_2_response = requests.get(
            PREFIX + "/" + postnewexam_2_response_json["id"], 
            headers=headers,
            verify=False
        )
        assert getexam_2_response.status_code == 200
        getexamtemplate_response = requests.get(
            PREFIX + "/" + postnewtemplate_response_json["id"], 
            headers=headers,
            verify=False
        )
        assert getexamtemplate_response.status_code == 404

    # cleanup
    finally:
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers,
                verify=False
            )
            assert deletepatient_1_response.status_code == 204
        if postnewexam_2_response.status_code == 201:
            deleteexam_2_response = requests.delete(
                PREFIX + "/" + postnewexam_2_response_json["id"], 
                headers=headers,
                verify=False
            )
            assert deleteexam_2_response.status_code == 204


def test_update_exam():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        postpatient_1A_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1A_response.status_code == 201
        postpatient_1A_response_json = postpatient_1A_response.json()
        exam = EXAM_TEMPLATE.copy()
        exam["patient_id"] = postpatient_1_response_json["id"]
        exam["is_template"] = False
        postexam_response = requests.post(PREFIX + "/new", json=exam, headers=headers, verify=False)
        assert postexam_response.status_code == 201
        update_request_1 = {
            "patient_id": postpatient_1A_response_json["id"],
            "name": "Automated test exam updated",
            "description": "Some test description updated",
            "indication": "Test indictation updated",
            "patient_height_cm": 111,
            "patient_weight_kg": 222,
            "comment": "updated comment",
            "status": "UPDATED",
            "is_template": False
        }
        update_request_2 = update_request_1.copy()
        update_request_2["status"] = "NEW"
        update_request_3 = update_request_1.copy()
        update_request_3["patient_id"] = "4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5"

        # TODO implement more conditions like in test_create_exam_from_template

    # act
        postexam_response_json = postexam_response.json()
        updateexam_response = requests.put(
            PREFIX + "/" + postexam_response_json["id"],
            json=update_request_1,
            headers=headers,
            verify=False
        )

    # check
        assert updateexam_response.status_code == 200
        updateexam_response = updateexam_response.json()
        for key in update_request_1.keys():
            assert updateexam_response[key] == update_request_1[key]
        getexam_response = requests.get(
            PREFIX + "/" + postexam_response_json["id"],
            headers=headers,
            verify=False)
        assert getexam_response.status_code == 200
        getexam_response_json = getexam_response.json()
        for key in update_request_1.keys():
            if key != "status":
                assert getexam_response_json[key] == update_request_1[key]

    # act
        updateexam_2_response = requests.put(
            PREFIX + "/" + postexam_response_json["id"], 
            json=update_request_2, 
            headers=headers,
            verify=False
        )
    # check
        assert updateexam_2_response.status_code == 403, \
            "Update status to NEW should be rejected."

    # act
        updateexam_3_response = requests.put(
            PREFIX + "/" + postexam_response_json["id"], 
            json=update_request_3, 
            headers=headers,
            verify=False
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
                headers=headers,
                verify=False)
            assert deleteexam_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers,
                verify=False)
            assert deletepatient_1_response.status_code == 204
        if postpatient_1A_response.status_code == 201:
            deletepatient_1A_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1A_response_json["id"]),
                headers=headers,
                verify=False)
            assert deletepatient_1A_response.status_code == 204


def test_create_workflow():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam = EXAM_TEMPLATE.copy()
        exam["patient_id"] = postpatient_1_response_json["id"]
        exam["is_template"] = False
        exam_template = EXAM_TEMPLATE.copy()
        postexam_response = requests.post(PREFIX + "/new", json=exam, headers=headers, verify=False)
        postexamtemplate_response = requests.post(
            PREFIX + "/new", json=exam_template, headers=headers, verify=False)
        assert postexam_response.status_code == 201
        postexam_response_json = postexam_response.json()
        assert postexamtemplate_response.status_code == 201
        postexamtemplate_response_json = postexamtemplate_response.json()
        workflow_1 = WORKFLOW_TEMPLATE.copy()
        workflow_1["is_template"] = False    # no exam id here
        workflow_2 = workflow_1.copy()
        workflow_2["exam_id"] = "4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5"
        workflow_3 = workflow_1.copy()
        workflow_3["exam_id"] = postexam_response_json["id"]
        workflow_4 = workflow_3.copy()
        workflow_4["is_template"] = True
        workflow_5 = workflow_3.copy()
        workflow_5["exam_id"] = postexamtemplate_response_json["id"]
        workflow_6 = workflow_3.copy()
        workflow_6["status"] = "UPDATED"

    # act
        postworkflow_response_1 = requests.post(
            PREFIX + "/workflow/new", json=workflow_1, headers=headers, verify=False)
        postworkflow_response_2 = requests.post(
            PREFIX + "/workflow/new", json=workflow_2, headers=headers, verify=False)
        postworkflow_response_3 = requests.post(
            PREFIX + "/workflow/new", json=workflow_3, headers=headers, verify=False)
        postworkflow_response_4 = requests.post(
            PREFIX + "/workflow/new", json=workflow_4, headers=headers, verify=False)
        postworkflow_response_5 = requests.post(
            PREFIX + "/workflow/new", json=workflow_5, headers=headers, verify=False)
        postworkflow_response_6 = requests.post(
            PREFIX + "/workflow/new", json=workflow_6, headers=headers, verify=False)

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
        assert postworkflow_response_6.status_code == 400, \
            "New with status != NEW should be rejected."
        postworkflow_response_json_3 = postworkflow_response_3.json()
        for key in workflow_3.keys():
            assert postworkflow_response_json_3[key] == workflow_3[key]
        getworkflow_response = requests.get(
            PREFIX + "/workflow/" + postworkflow_response_json_3["id"],
            headers=headers,
            verify=False)
        assert getworkflow_response.status_code == 200
        getworkflow_response_json = getworkflow_response.json()
        for key in workflow_3.keys():
            assert getworkflow_response_json[key] == workflow_3[key]

    # cleanup
    finally:
        if postexam_response.status_code == 201:
            deleteexam_response = requests.delete(
                PREFIX + "/" + postexam_response_json["id"], headers=headers, verify=False)
            assert deleteexam_response.status_code == 204
        if postexamtemplate_response.status_code == 201:
            postexamtemplate_response_json = postexamtemplate_response.json()
            deleteexamtemplate_response = requests.delete(
                PREFIX + "/" + postexamtemplate_response_json["id"], headers=headers, verify=False)
            assert deleteexamtemplate_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers,
                verify=False)
            assert deletepatient_1_response.status_code == 204
        # deleting an exam, recursively deletes the corresponding workflows


def test_create_workflow_from_template():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam = EXAM_TEMPLATE.copy()
        exam["patient_id"] = postpatient_1_response_json["id"]
        exam["is_template"] = False
        postexam_response = requests.post(PREFIX + "/new", json=exam, headers=headers, verify=False)
        assert postexam_response.status_code == 201
        postexam_response_json = postexam_response.json()
        exam_template = EXAM_TEMPLATE.copy()
        postexamtemplate_response = requests.post(
            PREFIX + "/new", json=exam_template, headers=headers, verify=False)
        assert postexamtemplate_response.status_code == 201
        postexamtemplate_response_json = postexamtemplate_response.json()
        workflow_template = WORKFLOW_TEMPLATE.copy()
        workflow_template["exam_id"] = postexamtemplate_response_json["id"]
        postnewtemplate_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template, headers=headers, verify=False)
        assert postnewtemplate_response.status_code == 201
        postnewtemplate_response_json = postnewtemplate_response.json()
        workflow = WORKFLOW_TEMPLATE.copy()
        workflow["exam_id"] = postexam_response_json["id"]
        workflow["is_template"] = False
        postworkflow_response = requests.post(
            PREFIX + "/workflow/new", json=workflow, headers=headers, verify=False)
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
            headers=headers,
            verify=False)
        postworkflowfromtemplate_fail_1_response = requests.post(
            PREFIX + "/workflow",
            params={
                "exam_id": postexam_response_json["id"], 
                "template_id": postworkflow_response_json["id"],
                "new_workflow_is_template": False   # could also check with True
            },
            headers=headers,
            verify=False)
        postworkflowfromtemplate_fail_2_response = requests.post(
            PREFIX + "/workflow",
            params={
                "exam_id": "4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5", 
                "template_id": postnewtemplate_response_json["id"],
                "new_workflow_is_template": False   # could also check with True
            },
            headers=headers,
            verify=False)
        postworkflowfromtemplate_fail_3_response = requests.post(
            PREFIX + "/workflow",
            params={
                "exam_id": postexam_response_json["id"], 
                "template_id": postnewtemplate_response_json["id"],
                "new_workflow_is_template": True
            },
            headers=headers,
            verify=False)
        postworkflowtemplatefromtemplate_response = requests.post(
            PREFIX + "/workflow",
            params={
                "exam_id": postexamtemplate_response_json["id"], 
                "template_id": postnewtemplate_response_json["id"],
                "new_workflow_is_template": True
            },
            headers=headers,
            verify=False)

    # check
        assert postworkflowfromtemplate_response.status_code == 201
        postworkflowfromtemplate_response_json = \
            postworkflowfromtemplate_response.json()
        for key in workflow_template.keys():
            if key != "is_template" and key != "exam_id":
                assert postworkflowfromtemplate_response_json[key] == \
                    workflow_template[key]
        assert postworkflowfromtemplate_response_json["exam_id"] == \
            postexam_response_json["id"]
        assert postworkflowfromtemplate_response_json["is_template"] is False
        getworkflow_response = requests.get(
            PREFIX + "/workflow/" + postworkflowfromtemplate_response_json["id"], 
            headers=headers,
            verify=False)
        assert getworkflow_response.status_code == 200
        getworkflow_response_json = getworkflow_response.json()
        for key in workflow_template.keys():
            if key != "is_template" and key != "exam_id":
                assert getworkflow_response_json[key] == workflow_template[key]
        assert getworkflow_response_json["exam_id"] == \
            postexam_response_json["id"]
        assert getworkflow_response_json["is_template"] is False
        assert postworkflowfromtemplate_fail_1_response.status_code == 400, \
            "Creating workflow from workflow instance should be rejected."
        assert postworkflowfromtemplate_fail_2_response.status_code == 400, \
            "exam_id must refer to an existing exam."
        assert postworkflowfromtemplate_fail_3_response.status_code == 400, \
            "Creating workflow template that links to exam instance should be rejected."
        assert postworkflowtemplatefromtemplate_response.status_code == 201

    # prepare
        updated_workflow_template = workflow_template.copy()
        updated_workflow_template["name"] = "Atomated test workflow template updated"
        updated_workflow_template["status"] = "UPDATED"
        putupdatedworkflowtemplate_response = requests.put(
            PREFIX + "/workflow/" + postworkflow_response_json["id"],
            json=updated_workflow_template,
            headers=headers,
            verify=False)
        assert putupdatedworkflowtemplate_response.status_code == 200

    # act
        postworkflowfromupdatedtemplate_response = requests.post(
            PREFIX + "/workflow",
            params={
                "exam_id": postexam_response_json["id"], 
                "template_id": putupdatedworkflowtemplate_response.json()["id"],
                "new_workflow_is_template": False   # could also check with True
            },
            headers=headers,
            verify=False)

    # check
        assert postworkflowfromupdatedtemplate_response.status_code == 201
        assert postworkflowfromupdatedtemplate_response.json()["status"] == "NEW", \
            "status of new workflow should be NEW independent of the templates status."

    # cleanup
    finally:
        # deleting exam recursively deletes associated workflows
        deleteexam_response = requests.delete(
            PREFIX + "/" + postexam_response_json["id"], headers=headers, verify=False)
        assert deleteexam_response.status_code == 204
        if postexamtemplate_response.status_code == 201:
            deleteexamtemplate_response = requests.delete(
                PREFIX + "/" + postexamtemplate_response_json["id"], headers=headers, verify=False)
            assert deleteexamtemplate_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers,
                verify=False)
            assert deletepatient_1_response.status_code == 204


def test_get_workflow():
    # Successfully getting a workflow is already tested in test_create_workflow.
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    getworkflow_response = requests.get(PREFIX + "/workflow/123", headers=headers, verify=False)
    assert getworkflow_response.status_code == 400   # invalid uuid format
    getworkflow_response = requests.get(
        PREFIX + "/workflow/4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5", headers=headers, verify=False)
    assert getworkflow_response.status_code == 404


def test_get_all_exam_workflows():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam1 = EXAM_TEMPLATE.copy()
        exam1["patient_id"] = postpatient_1_response_json["id"]
        exam1["is_template"] = False
        exam2 = exam1.copy()
        exam2["site"] = "test site 2"
        postnewexam1_response = requests.post(
            PREFIX + "/new", json=exam1, headers=headers, verify=False)
        postnewexam2_response = requests.post(
            PREFIX + "/new", json=exam2, headers=headers, verify=False)
        assert postnewexam1_response.status_code == 201
        assert postnewexam2_response.status_code == 201
        postnewexam1_response_json = postnewexam1_response.json()
        postnewexam2_response_json = postnewexam2_response.json()
        workflow_1 = WORKFLOW_TEMPLATE.copy()
        workflow_1["exam_id"] = postnewexam1_response_json["id"]
        workflow_1["is_template"] = False
        workflow_2 = workflow_1.copy()
        workflow_2["name"] = "Automated test workflow 2"
        workflow_3 = workflow_1.copy()
        workflow_3["name"] = "Automated test workflow 3"
        workflow_3["exam_id"] = postnewexam2_response_json["id"]
        postworkflow_1_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_1, headers=headers, verify=False)
        postworkflow_2_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_2, headers=headers, verify=False)
        postworkflow_3_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_3, headers=headers, verify=False)
        assert postworkflow_1_response.status_code == 201
        assert postworkflow_2_response.status_code == 201
        assert postworkflow_3_response.status_code == 201

    # act
        getallworkflows_response = requests.get(
            PREFIX + "/workflow/all/" + str(postnewexam1_response_json["id"]), 
            headers=headers, verify=False)
        # could enforce error when requesting workflows for non existing exam
        # getallworkflowswrongid_response = requests.get(
        #     PREFIX + "/workflow/all/4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5", 
        #     headers=headers, verify=False)

    # check
        assert getallworkflows_response.status_code == 200
        getallworkflows_response_json = getallworkflows_response.json()
        assert len(getallworkflows_response_json) == 2
        def workflow_in_response(workflow):
            for workflow_json_found in getallworkflows_response_json:
                workflow_matches = True
                for key in workflow.keys():
                    if workflow[key] != workflow_json_found[key]:
                        workflow_matches = False
                if workflow_matches:
                    return True
            return False
        assert workflow_in_response(workflow_1)
        assert workflow_in_response(workflow_2)
        assert not workflow_in_response(workflow_3)
        # could enforce error when requesting workflows for non existing exam
        # assert getallworkflowswrongid_response.status_code == 404

    # cleanup
    finally:
        if postnewexam1_response.status_code == 201:
            deleteexam1_response = requests.delete(
                PREFIX + "/" + postnewexam1_response.json()["id"], headers=headers, verify=False)
            assert deleteexam1_response.status_code == 204
        if postnewexam2_response.status_code == 201:
            deleteexam2_response = requests.delete(
                PREFIX + "/" + postnewexam2_response.json()["id"], headers=headers, verify=False)
            assert deleteexam2_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers, verify=False)
            assert deletepatient_1_response.status_code == 204


def test_get_all_workflow_templates():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    exam_template_1 = EXAM_TEMPLATE.copy()
    exam_template_2 = exam_template_1.copy()
    exam_template_2["site"] = "template 2 site"
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam_1 = exam_template_1.copy()
        exam_1["is_template"] = False
        exam_1["patient_id"] = postpatient_1_response_json["id"]
        getallworkflowtemplatesbefore_response = requests.get(
            PREFIX + "/workflow/templates/all",
            headers=headers,
            verify=False)
        assert getallworkflowtemplatesbefore_response.status_code == 200

        postnewexamtemplate_1_response = requests.post(
            PREFIX + "/new", json=exam_template_1, headers=headers, verify=False)
        assert postnewexamtemplate_1_response.status_code == 201
        postnewexamtemplate_1_response_json = postnewexamtemplate_1_response.json()
        postnewexamtemplate_2_response = requests.post(
            PREFIX + "/new", json=exam_template_2, headers=headers, verify=False)
        assert postnewexamtemplate_2_response.status_code == 201
        postnewexamtemplate_2_response_json = postnewexamtemplate_2_response.json()
        postnewexam_1_response = requests.post(
            PREFIX + "/new", json=exam_1, headers=headers, verify=False)
        assert postnewexam_1_response.status_code == 201
        postnewexam_1_response_json = postnewexam_1_response.json()
        workflow_template_1 = WORKFLOW_TEMPLATE.copy()
        workflow_template_1["exam_id"] = postnewexamtemplate_1_response_json["id"]
        workflow_template_2 = workflow_template_1.copy()
        workflow_template_2["name"] = "Automated test workflow template 2"
        workflow_template_3 = workflow_template_1.copy()
        workflow_template_3["name"] = "Automated test workflow template 3"
        workflow_template_3["exam_id"] = postnewexamtemplate_2_response_json["id"]
        workflow_1 = workflow_template_1.copy()
        workflow_1["name"] = "Automated test workflow 1"
        workflow_1["exam_id"] = postnewexam_1_response_json["id"]
        workflow_1["is_template"] = False
        postworkflowtemplate_1_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template_1, headers=headers, verify=False)
        postworkflowtemplate_2_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template_2, headers=headers, verify=False)
        postworkflowtemplate_3_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template_3, headers=headers, verify=False)
        postworkflow_1_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_1, headers=headers, verify=False)
        assert postworkflowtemplate_1_response.status_code == 201
        assert postworkflowtemplate_2_response.status_code == 201
        assert postworkflowtemplate_3_response.status_code == 201
        assert postworkflow_1_response.status_code == 201  # does not count to templates

    # act
        getallworkflowtemplates_response = requests.get(
            PREFIX + "/workflow/templates/all",
            headers=headers,
            verify=False)

    # check
        assert getallworkflowtemplates_response.status_code == 200
        getallworkflowtemplates_response_json = \
            getallworkflowtemplates_response.json()
        assert len(getallworkflowtemplates_response_json) \
            - len(getallworkflowtemplatesbefore_response.json()) == 3
        
        def workflow_template_in_received_list(workflow_template):
            for workflow_template_json_found in getallworkflowtemplates_response_json:
                assert workflow_template_json_found["is_template"] is True
                workflow_template_matches = True
                for key in workflow_template.keys():
                    if workflow_template[key] != workflow_template_json_found[key]:
                        workflow_template_matches = False
                if workflow_template_matches:
                    return True
            return False

        assert workflow_template_in_received_list(workflow_template_1)
        assert workflow_template_in_received_list(workflow_template_2)
        assert workflow_template_in_received_list(workflow_template_3)

    # cleanup
    finally:
        if postnewexamtemplate_1_response.status_code == 201:
            deleteexamtemplate_1_presponse = requests.delete(
                PREFIX + "/" + postnewexamtemplate_1_response_json["id"],
                headers=headers,
                verify=False
            )
            assert deleteexamtemplate_1_presponse.status_code == 204
        if postnewexamtemplate_2_response.status_code == 201:
            deleteexamtemplate_2_presponse = requests.delete(
                PREFIX + "/" + postnewexamtemplate_2_response_json["id"],
                headers=headers,
                verify=False
            )
            assert deleteexamtemplate_2_presponse.status_code == 204
        if postnewexam_1_response.status_code == 201:
            deleteexam_1_presponse = requests.delete(
                PREFIX + "/" + postnewexam_1_response_json["id"],
                headers=headers,
                verify=False
            )
            assert deleteexam_1_presponse.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers,
                verify=False)
            assert deletepatient_1_response.status_code == 204


def test_delete_workflow():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam = EXAM_TEMPLATE.copy()
        exam["patient_id"] = postpatient_1_response_json["id"]
        exam["is_template"] = False
        postnewexam_response = requests.post(
            PREFIX + "/new", json=exam, headers=headers, verify=False)
        assert postnewexam_response.status_code == 201
        postnewexam_response_json = postnewexam_response.json()
        exam_template = EXAM_TEMPLATE.copy()
        postnewexamtemplate_response = requests.post(
            PREFIX + "/new", json=exam_template, headers=headers, verify=False)
        assert postnewexamtemplate_response.status_code == 201
        postnewexamtemplate_response_json = postnewexamtemplate_response.json()
        workflow_1 = WORKFLOW_TEMPLATE.copy()
        workflow_1["exam_id"] = postnewexam_response_json["id"]
        workflow_1["is_template"] = False
        workflow_2 = workflow_1.copy()
        workflow_2["name"] = "Automated test workflow 2"
        workflow_template_1 = WORKFLOW_TEMPLATE.copy()
        workflow_template_1["exam_id"] = postnewexamtemplate_response_json["id"]
        postworkflow_1_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_1, headers=headers, verify=False)
        assert postworkflow_1_response.status_code == 201
        postworkflow_1_response_json = postworkflow_1_response.json()
        postworkflow_2_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_2, headers=headers, verify=False)
        assert postworkflow_2_response.status_code == 201
        postworkflow_2_response_json = postworkflow_2_response.json()
        postworkflow_template_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template_1, headers=headers, verify=False)
        assert postworkflow_template_response.status_code == 201
        postworkflow_template_response_json = postworkflow_template_response.json()

    # act
        deleteworkflow_1_response = requests.delete(
            PREFIX + "/workflow/" + postworkflow_1_response_json["id"], 
            headers=headers,
            verify=False
        )
        deleteworkflow_template_response = requests.delete(
            PREFIX + "/workflow/" + postworkflow_template_response_json["id"], 
            headers=headers,
            verify=False
        )

    # check
        assert deleteworkflow_1_response.status_code == 204
        assert deleteworkflow_template_response.status_code == 204
        getworkflow_1_response = requests.get(
            PREFIX + "/workflow/" + postworkflow_1_response_json["id"],
            headers=headers,
            verify=False)
        assert getworkflow_1_response.status_code == 404
        getworkflow_2_response = requests.get(
            PREFIX + "/workflow/" + postworkflow_2_response_json["id"],
            headers=headers,
            verify=False)
        assert getworkflow_2_response.status_code == 200
        getworkflowtemplate_response = requests.get(
            PREFIX + "/" + postworkflow_template_response_json["id"],
            headers=headers,
            verify=False)
        assert getworkflowtemplate_response.status_code == 404

    # cleanup
    finally:
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers,
                verify=False)
            assert deletepatient_1_response.status_code == 204
        if postnewexam_response.status_code == 201:
            deleteexam_response = requests.delete(
                PREFIX + "/" + postnewexam_response_json["id"],
                headers=headers,
                verify=False
            )
            assert deleteexam_response.status_code == 204
        if postnewexamtemplate_response.status_code:
            deleteexamtemplate_presponse = requests.delete(
                PREFIX + "/" + postnewexamtemplate_response_json["id"],
                headers=headers,
                verify=False
            )
            assert deleteexamtemplate_presponse.status_code == 204


def test_update_workflow():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam_1 = EXAM_TEMPLATE.copy()
        exam_1["patient_id"] = postpatient_1_response_json["id"]
        exam_1["is_template"] = False
        postexam_1_response = requests.post(
            PREFIX + "/new", json=exam_1, headers=headers, verify=False)
        assert postexam_1_response.status_code == 201
        postexam_1_response_json = postexam_1_response.json()
        exam_2 = exam_1.copy()
        exam_2["name"] = "Automated test exam 2"
        postexam_2_response = requests.post(
            PREFIX + "/new", json=exam_2, headers=headers, verify=False)
        assert postexam_2_response.status_code == 201
        postexam_2_response_json = postexam_2_response.json()
        workflow = WORKFLOW_TEMPLATE.copy()
        workflow["exam_id"] = postexam_1_response_json["id"]
        workflow["is_template"] = False
        postworkflow_response = requests.post(
            PREFIX + "/workflow/new", json=workflow, headers=headers, verify=False)
        assert postworkflow_response.status_code == 201
        postworkflow_response_json = postworkflow_response.json()
        update_request_1 = {
            "exam_id": postexam_2_response_json["id"],
            "name": "Automated test workflow updated",
            "description": "test description updated",
            "comment": "test comment updated",
            "status": "UPDATED",
            "is_template": False,
        }
        update_request_2 = update_request_1.copy()
        update_request_2["status"] = "NEW"
        update_request_3 = update_request_1.copy()
        update_request_3["exam_id"] = "4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5"
        update_request_4 = update_request_1.copy()
        update_request_4["is_template"] = True
        # TODO implement more conditions like in test_create_exam_from_template

    # act
        updateworkflow_response_1 = requests.put(
            PREFIX + "/workflow/" + postworkflow_response_json["id"],
            json=update_request_1,
            headers=headers,
            verify=False
        )

    # check
        assert updateworkflow_response_1.status_code == 200
        updateworkflow_response_1_json = updateworkflow_response_1.json()
        for key in update_request_1.keys():
            assert updateworkflow_response_1_json[key] == update_request_1[key]
        getworkflow_response_1 = requests.get(
            PREFIX + "/workflow/" + postworkflow_response_json["id"],
            headers=headers,
            verify=False)
        assert getworkflow_response_1.status_code == 200
        getworkflow_response_1_json = getworkflow_response_1.json()
        for key in update_request_1.keys():
            if key != "status":
                assert getworkflow_response_1_json[key] == update_request_1[key]

    # act
        updateworkflow_response_2 = requests.put(
            PREFIX + "/workflow/" + postworkflow_response_json["id"],
            json=update_request_2,
            headers=headers,
            verify=False
        )
    # check
        assert updateworkflow_response_2.status_code == 403, \
            "Update status to NEW should be rejected."

    # act
        updateworkflow_response_3 = requests.put(
            PREFIX + "/workflow/" + postworkflow_response_json["id"],
            json=update_request_3,
            headers=headers,
            verify=False
        )
    # check
        assert updateworkflow_response_3.status_code == 400, \
            "Wrong exam_id should be rejected."

    # act
        updateworkflow_response_4 = requests.put(
            PREFIX + "/workflow/" + postworkflow_response_json["id"],
            json=update_request_4,
            headers=headers,
            verify=False
        )
    # check
        assert updateworkflow_response_4.status_code == 400, \
            "Update to template with reference to exam instance should be rejected."

    # cleanup
    finally:
        if postexam_1_response.status_code == 201:
            deleteexam_1_response = requests.delete(
                PREFIX + "/" + 
                postexam_1_response_json["id"],
                headers=headers,
                verify=False)
            assert deleteexam_1_response.status_code == 204
        if postexam_2_response.status_code == 201:
            deleteexam_2_response = requests.delete(
                PREFIX + "/" + 
                postexam_2_response_json["id"],
                headers=headers,
                verify=False)
            assert deleteexam_2_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers,
                verify=False)
            assert deletepatient_1_response.status_code == 204


def test_create_task():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam = EXAM_TEMPLATE.copy()
        exam["patient_id"] = postpatient_1_response_json["id"]
        exam["is_template"] = False
        exam_template = EXAM_TEMPLATE.copy()
        postexam_response = requests.post(PREFIX + "/new", json=exam, headers=headers, verify=False)
        postexamtemplate_response = requests.post(
            PREFIX + "/new", json=exam_template, headers=headers, verify=False)
        assert postexam_response.status_code == 201
        postexam_response_json = postexam_response.json()
        assert postexamtemplate_response.status_code == 201
        postexamtemplate_response_json = postexamtemplate_response.json()
        workflow_1 = WORKFLOW_TEMPLATE.copy()
        workflow_1["exam_id"] = postexam_response_json["id"]
        workflow_1["is_template"] = False
        workflow_template_1 = WORKFLOW_TEMPLATE.copy()
        workflow_template_1["exam_id"] = postexamtemplate_response_json["id"]
        postworkflow_1_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_1, headers=headers, verify=False)
        postworkflowtemplate_1_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template_1, headers=headers, verify=False)
        assert postworkflow_1_response.status_code == 201
        assert postworkflowtemplate_1_response.status_code == 201
        postworkflow_1_response_json = postworkflow_1_response.json()
        postworkflowtemplate_1_response_json = postworkflowtemplate_1_response.json()
        task_1 = TASK_TEMPLATE.copy()
        task_1["workflow_id"] = postworkflow_1_response_json["id"]
        task_1["is_template"] = False
        task_2 = task_1.copy()
        task_2["workflow_id"] = "4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5"
        task_3 = task_1.copy()
        task_3["workflow_id"] = None
        task_4 = task_1.copy()
        task_4["is_template"] = True
        task_5 = task_1.copy()
        task_5["workflow_id"] = postworkflowtemplate_1_response_json["id"]
        task_6 = task_1.copy()
        task_6["status"] = "STARTED"

    # act
        posttask_1_response = requests.post(
            PREFIX + "/task/new", json=task_1, headers=headers, verify=False)
        posttask_2_response = requests.post(
            PREFIX + "/task/new", json=task_2, headers=headers, verify=False)
        posttask_3_response = requests.post(
            PREFIX + "/task/new", json=task_3, headers=headers, verify=False)
        posttask_4_response = requests.post(
            PREFIX + "/task/new", json=task_4, headers=headers, verify=False)
        posttask_5_response = requests.post(
            PREFIX + "/task/new", json=task_5, headers=headers, verify=False)
        posttask_6_response = requests.post(
            PREFIX + "/task/new", json=task_6, headers=headers, verify=False)

    # check
        assert posttask_1_response.status_code == 201
        posttask_1_response_json = posttask_1_response.json()
        for key in task_1.keys():
            assert posttask_1_response_json[key] == task_1[key]
        gettask_1_response = requests.get(
            PREFIX + "/task/" + posttask_1_response_json["id"], headers=headers, verify=False)
        assert gettask_1_response.status_code == 200
        gettask_1_response_json = gettask_1_response.json()
        for key in task_1.keys():
            assert gettask_1_response_json[key] == task_1[key]
        input_json = json.loads(gettask_1_response_json["artifacts"]["input"])
        output_json = json.loads(gettask_1_response_json["artifacts"]["output"])
        assert input_json[0]["path"] == "/data"
        assert input_json[0]["name"] == "inputfile2"
        assert output_json[0]["path"] == "/data"
        assert output_json[0]["name"] == "outputfile1"
        assert posttask_2_response.status_code == 400, \
            "Task with wrong workflow_id should be rejected."
        assert posttask_3_response.status_code == 400, \
            "Task without workflow_id should be rejected."
        assert posttask_4_response.status_code == 400, \
            "Task template that refers to workflow instance should be rejected."
        assert posttask_5_response.status_code == 400, \
            "Task instance that refers to workflow template should be rejected."
        assert posttask_6_response.status_code == 400, \
            'New task with status != {"PENDING": "..."} should be rejected.'

    # cleanup
    finally:
        if postexam_response.status_code == 201:
            deleteexam_response = requests.delete(
                PREFIX + "/" + postexam_response_json["id"], headers=headers, verify=False)
            assert deleteexam_response.status_code == 204
        if postexamtemplate_response.status_code == 201:
            postexamtemplate_response_json = postexamtemplate_response.json()
            deleteexamtemplate_response = requests.delete(
                PREFIX + "/" + postexamtemplate_response_json["id"], headers=headers, verify=False)
            assert deleteexamtemplate_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers, verify=False)
            assert deletepatient_1_response.status_code == 204
        # deleting an exam, recursively deletes the corresponding workflows and tasks


def test_create_task_from_template():
    # TODO work in progress
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam = EXAM_TEMPLATE.copy()
        exam["patient_id"] = postpatient_1_response_json["id"]
        exam["is_template"] = False
        postexam_response = requests.post(PREFIX + "/new", json=exam, headers=headers, verify=False)
        assert postexam_response.status_code == 201
        postexam_response_json = postexam_response.json()
        exam_template = EXAM_TEMPLATE.copy()
        postexamtemplate_response = requests.post(
            PREFIX + "/new", json=exam_template, headers=headers, verify=False)
        assert postexamtemplate_response.status_code == 201
        postexamtemplate_response_json = postexamtemplate_response.json()
        workflow_template = WORKFLOW_TEMPLATE.copy()
        workflow_template["exam_id"] = postexamtemplate_response_json["id"]
        postworkflowtemplate_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template, headers=headers, verify=False)
        assert postworkflowtemplate_response.status_code == 201
        postworkflowtemplate_response_json = postworkflowtemplate_response.json()
        workflow = WORKFLOW_TEMPLATE.copy()
        workflow["exam_id"] = postexam_response_json["id"]
        workflow["is_template"] = False
        postworkflow_response = requests.post(
            PREFIX + "/workflow/new", json=workflow, headers=headers, verify=False)
        assert postworkflow_response.status_code == 201
        postworkflow_response_json = postworkflow_response.json()
        task_template = TASK_TEMPLATE.copy()
        task_template["workflow_id"] = postworkflowtemplate_response_json["id"]
        posttasktemplate_response = requests.post(
            PREFIX + "/task/new", json=task_template, headers=headers, verify=False)
        assert posttasktemplate_response.status_code == 201
        posttasktemplate_response_json = posttasktemplate_response.json()
        task = task_template.copy()
        task["workflow_id"] = postworkflow_response_json["id"]
        task["name"] = "Automated test task"
        task["is_template"] = False
        posttask_response = requests.post(
            PREFIX + "/task/new", json=task, headers=headers, verify=False)
        assert posttask_response.status_code == 201
        posttask_response_json = posttask_response.json()

    # act
        posttaskfromtemplate_response = requests.post(
            PREFIX + "/task",
            params={
                "workflow_id": postworkflow_response_json["id"], 
                "template_id": posttasktemplate_response_json["id"],
                "new_task_is_template": False   # could also check with True
            },
            headers=headers,
            verify=False)
        posttaskfromtemplate_fail_1_response = requests.post(
            PREFIX + "/task",
            params={
                "workflow_id": postworkflow_response_json["id"], 
                "template_id": posttask_response_json["id"],
                "new_task_is_template": False   # could also check with True
            },
            headers=headers, verify=False)
        posttaskfromtemplate_fail_2_response = requests.post(
            PREFIX + "/task",
            params={
                "workflow_id": "4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5", 
                "template_id": posttasktemplate_response_json["id"],
                "new_task_is_template": False   # could also check with True
            },
            headers=headers, verify=False)
        posttaskfromtemplate_fail_3_response = requests.post(
            PREFIX + "/task",
            params={
                "workflow_id": posttask_response_json["id"], 
                "template_id": posttasktemplate_response_json["id"],
                "new_task_is_template": True
            },
            headers=headers, verify=False)
        posttasktemplatefromtemplate_response = requests.post(
            PREFIX + "/task",
            params={
                "workflow_id": postworkflowtemplate_response_json["id"], 
                "template_id": posttasktemplate_response_json["id"],
                "new_task_is_template": True
            },
            headers=headers, verify=False)

    # check
        assert posttaskfromtemplate_response.status_code == 201
        posttaskfromtemplate_response_json = posttaskfromtemplate_response.json()
        for key in task_template.keys():
            if key != "is_template" and key != "workflow_id":
                assert posttaskfromtemplate_response_json[key] == task_template[key]
        assert posttaskfromtemplate_response_json["workflow_id"] == \
            postworkflow_response_json["id"]
        assert posttaskfromtemplate_response_json["is_template"] is False
        gettask_response = requests.get(
            PREFIX + "/task/" + posttaskfromtemplate_response_json["id"], 
            headers=headers, verify=False)
        assert gettask_response.status_code == 200
        gettask_response_json = gettask_response.json()
        for key in task_template.keys():
            if key != "is_template" and key != "workflow_id":
                assert gettask_response_json[key] == task_template[key]
        assert gettask_response_json["workflow_id"] == postworkflow_response_json["id"]
        assert gettask_response_json["is_template"] is False
        assert posttaskfromtemplate_fail_1_response.status_code == 400, \
            "Creating task from task instance should be rejected."
        assert posttaskfromtemplate_fail_2_response.status_code == 400, \
            "exam_id must refer to an existing exam."
        assert posttaskfromtemplate_fail_3_response.status_code == 400, \
            "Creating task template that links to task instance should be rejected."
        assert posttasktemplatefromtemplate_response.status_code == 201

    # prepare
        # updated_workflow_template = workflow_template.copy()
        # updated_workflow_template["name"] = "Atomated test workflow template updated"
        # updated_workflow_template["status"] = "UPDATED"
        # putupdatedworkflowtemplate_response = requests.put(
        #     PREFIX + "/workflow/" + postworkflow_response_json["id"],
        #     json=updated_workflow_template,
        #     headers=headers, verify=False)
        # assert putupdatedworkflowtemplate_response.status_code == 200

    # act
        # postworkflowfromupdatedtemplate_response = requests.post(
        #     PREFIX + "/workflow",
        #     params={
        #         "exam_id": postexam_response_json["id"], 
        #         "template_id": putupdatedworkflowtemplate_response.json()["id"],
        #         "new_workflow_is_template": False   # could also check with True
        #     },
        #     headers=headers, verify=False)

    # check
        # assert postworkflowfromupdatedtemplate_response.status_code == 201
        # assert postworkflowfromupdatedtemplate_response.json()["status"] == "NEW", \
        #    "status of new workflow should be NEW independent of the templates status."

    # cleanup
    finally:
        # deleting exam recursively deletes associated workflows and tasks
        deleteexam_response = requests.delete(
            PREFIX + "/" + postexam_response_json["id"], headers=headers, verify=False)
        assert deleteexam_response.status_code == 204
        if postexamtemplate_response.status_code == 201:
            deleteexamtemplate_response = requests.delete(
                PREFIX + "/" + postexamtemplate_response_json["id"], headers=headers, verify=False)
            assert deleteexamtemplate_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers, verify=False)
            assert deletepatient_1_response.status_code == 204


def test_get_task():
    # Successfully getting a task is already tested in test_create_task.
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    gettask_response = requests.get(PREFIX + "/task/123", headers=headers, verify=False)
    assert gettask_response.status_code == 400   # invalid uuid format
    gettask_response = requests.get(
        PREFIX + "/task/4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5", headers=headers, verify=False)
    assert gettask_response.status_code == 404


def test_get_all_workflow_tasks():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam = EXAM_TEMPLATE.copy()
        exam["patient_id"] = postpatient_1_response_json["id"]
        exam["is_template"] = False
        postnewexam_response = requests.post(
            PREFIX + "/new", json=exam, headers=headers, verify=False)
        assert postnewexam_response.status_code == 201
        postnewexam_response_json = postnewexam_response.json()
        workflow_1 = WORKFLOW_TEMPLATE.copy()
        workflow_1["exam_id"] = postnewexam_response_json["id"]
        workflow_1["is_template"] = False
        workflow_2 = workflow_1.copy()
        workflow_2["name"] = "Automated test workflow 2"
        postworkflow_1_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_1, headers=headers, verify=False)
        postworkflow_2_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_2, headers=headers, verify=False)
        assert postworkflow_1_response.status_code == 201
        assert postworkflow_2_response.status_code == 201
        postworkflow_1_response_json = postworkflow_1_response.json()
        postworkflow_2_response_json = postworkflow_2_response.json()
        task_1 = TASK_TEMPLATE.copy()
        task_1["workflow_id"] = postworkflow_1_response_json["id"]
        task_1["is_template"] = False
        task_2 = task_1.copy()
        task_2["name"] = "Automated test task 2"
        task_3 = task_1.copy()
        task_3["name"] = "Automated test task 3"
        task_3["workflow_id"] = postworkflow_2_response_json["id"]
        posttask_1_response = requests.post(
            PREFIX + "/task/new", json=task_1, headers=headers, verify=False)
        posttask_2_response = requests.post(
            PREFIX + "/task/new", json=task_2, headers=headers, verify=False)
        posttask_3_response = requests.post(
            PREFIX + "/task/new", json=task_3, headers=headers, verify=False)
        assert posttask_1_response.status_code == 201
        assert posttask_2_response.status_code == 201
        assert posttask_3_response.status_code == 201

    # act
        getalltasks_response = requests.get(
            PREFIX + "/task/all/" + str(postworkflow_1_response_json["id"]), 
            headers=headers, verify=False)
        # could enforce error when requesting tasks for non existing workflow
        # getalltaskswrongid_response = requests.get(
        #     PREFIX + "/task/all/4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5", 
        #     headers=headers, verify=False)

    # check
        assert getalltasks_response.status_code == 200
        getalltasks_response_json = getalltasks_response.json()
        assert len(getalltasks_response_json) == 2
        def task_in_response(task):
            for task_json_found in getalltasks_response_json:
                task_matches = True
                for key in task.keys():
                    if task[key] != task_json_found[key]:
                        task_matches = False
                if task_matches:
                    return True
            return False
        assert task_in_response(task_1)
        assert task_in_response(task_2)
        assert not task_in_response(task_3)
        # could enforce error when requesting workflows for non existing exam
        # assert getallworkflowswrongid_response.status_code == 404

    # cleanup
    finally:
        if postnewexam_response.status_code == 201:
            deleteexam1_response = requests.delete(
                PREFIX + "/" + postnewexam_response.json()["id"], headers=headers, verify=False)
            assert deleteexam1_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers, verify=False)
            assert deletepatient_1_response.status_code == 204


def test_get_all_task_templates():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        exam_template_1 = EXAM_TEMPLATE.copy()
        exam_template_2 = exam_template_1.copy()
        exam_template_2["name"] = "Automated test template 2"
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam_1 = exam_template_1.copy()
        exam_1["is_template"] = False
        exam_1["patient_id"] = postpatient_1_response_json["id"]
        getalltasktemplatesbefore_response = requests.get(
            PREFIX + "/task/templates/all",
            headers=headers, verify=False)
        assert getalltasktemplatesbefore_response.status_code == 200
        postnewexamtemplate_1_response = requests.post(
            PREFIX + "/new", json=exam_template_1, headers=headers, verify=False)
        assert postnewexamtemplate_1_response.status_code == 201
        postnewexamtemplate_1_response_json = postnewexamtemplate_1_response.json()
        postnewexamtemplate_2_response = requests.post(
            PREFIX + "/new", json=exam_template_2, headers=headers, verify=False)
        assert postnewexamtemplate_2_response.status_code == 201
        postnewexamtemplate_2_response_json = postnewexamtemplate_2_response.json()
        postnewexam_1_response = requests.post(
            PREFIX + "/new", json=exam_1, headers=headers, verify=False)
        assert postnewexam_1_response.status_code == 201
        postnewexam_1_response_json = postnewexam_1_response.json()
        workflow_template_1 = WORKFLOW_TEMPLATE.copy()
        workflow_template_1["exam_id"] = postnewexamtemplate_1_response_json["id"]
        workflow_template_2 = workflow_template_1.copy()
        workflow_template_2["name"] = "Automated test workflow template 2"
        workflow_template_3 = workflow_template_1.copy()
        workflow_template_3["name"] = "Automated test workflow template 3"
        workflow_template_3["exam_id"] = postnewexamtemplate_2_response_json["id"]
        workflow_1 = workflow_template_1.copy()
        workflow_1["name"] = "Automated test workflow 1"
        workflow_1["exam_id"] = postnewexam_1_response_json["id"]
        workflow_1["is_template"] = False
        postworkflowtemplate_1_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template_1, headers=headers, verify=False)
        postworkflowtemplate_2_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template_2, headers=headers, verify=False)
        postworkflowtemplate_3_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template_3, headers=headers, verify=False)
        postworkflow_1_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_1, headers=headers, verify=False)
        assert postworkflowtemplate_1_response.status_code == 201
        assert postworkflowtemplate_2_response.status_code == 201
        assert postworkflowtemplate_3_response.status_code == 201
        assert postworkflow_1_response.status_code == 201
        postworkflowtemplate_1_response_json = postworkflowtemplate_1_response.json()
        postworkflowtemplate_2_response_json = postworkflowtemplate_2_response.json()
        postworkflowtemplate_3_response_json = postworkflowtemplate_3_response.json()
        postworkflow_1_response_json = postworkflow_1_response.json()
        task_template_1 = TASK_TEMPLATE.copy()
        task_template_1["workflow_id"] = postworkflowtemplate_1_response_json["id"]
        task_template_2 = task_template_1.copy()
        task_template_2["name"] = "Automated test task template 2"
        task_template_2["workflow_id"] = postworkflowtemplate_2_response_json["id"]
        task_template_3 = task_template_1.copy()
        task_template_3["name"] = "Automated test task template 3"
        task_template_3["workflow_id"] = postworkflowtemplate_3_response_json["id"]
        task_1 = task_template_1.copy()
        task_1["name"] = "Automated test task"
        task_1["is_template"] = False
        task_1["workflow_id"] = postworkflow_1_response_json["id"]
        posttasktemplate_1_response = requests.post(
            PREFIX + "/task/new", json=task_template_1, headers=headers, verify=False)
        posttasktemplate_2_response = requests.post(
            PREFIX + "/task/new", json=task_template_2, headers=headers, verify=False)
        posttasktemplate_3_response = requests.post(
            PREFIX + "/task/new", json=task_template_3, headers=headers, verify=False)
        posttask_1_response = requests.post(
            PREFIX + "/task/new", json=task_1, headers=headers, verify=False)
        assert posttasktemplate_1_response.status_code == 201
        assert posttasktemplate_2_response.status_code == 201
        assert posttasktemplate_3_response.status_code == 201
        assert posttask_1_response.status_code == 201

    # act
        getalltasktemplates_response = requests.get(
            PREFIX + "/task/templates/all",
            headers=headers, verify=False)

    # check
        assert getalltasktemplates_response.status_code == 200
        getalltasktemplates_response_json = getalltasktemplates_response.json()
        assert len(getalltasktemplates_response_json) \
            - len(getalltasktemplatesbefore_response.json()) == 3
        
        def task_template_in_received_list(task_template):
            for task_template_json_found in getalltasktemplates_response_json:
                assert task_template_json_found["is_template"] is True
                task_template_matches = True
                for key in task_template.keys():
                    if task_template[key] != task_template_json_found[key]:
                        task_template_matches = False
                if task_template_matches:
                    return True
            return False

        assert task_template_in_received_list(task_template_1)
        assert task_template_in_received_list(task_template_2)
        assert task_template_in_received_list(task_template_3)

    # cleanup
    finally:
        if postnewexamtemplate_1_response.status_code == 201:
            deleteexamtemplate_1_presponse = requests.delete(
                PREFIX + "/" + postnewexamtemplate_1_response_json["id"],
                headers=headers, verify=False,
            )
            assert deleteexamtemplate_1_presponse.status_code == 204
        if postnewexamtemplate_2_response.status_code == 201:
            deleteexamtemplate_2_presponse = requests.delete(
                PREFIX + "/" + postnewexamtemplate_2_response_json["id"],
                headers=headers, verify=False,
            )
            assert deleteexamtemplate_2_presponse.status_code == 204
        if postnewexam_1_response.status_code == 201:
            deleteexam_1_presponse = requests.delete(
                PREFIX + "/" + postnewexam_1_response_json["id"],
                headers=headers, verify=False,
            )
            assert deleteexam_1_presponse.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers, verify=False)
            assert deletepatient_1_response.status_code == 204


def test_delete_task():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam = EXAM_TEMPLATE.copy()
        exam["patient_id"] = postpatient_1_response_json["id"]
        exam["is_template"] = False
        postnewexam_response = requests.post(
            PREFIX + "/new", json=exam, headers=headers, verify=False)
        assert postnewexam_response.status_code == 201
        postnewexam_response_json = postnewexam_response.json()
        exam_template = EXAM_TEMPLATE.copy()
        postnewexamtemplate_response = requests.post(
            PREFIX + "/new", json=exam_template, headers=headers, verify=False)
        assert postnewexamtemplate_response.status_code == 201
        postnewexamtemplate_response_json = postnewexamtemplate_response.json()
        workflow_1 = WORKFLOW_TEMPLATE.copy()
        workflow_1["exam_id"] = postnewexam_response_json["id"]
        workflow_1["is_template"] = False
        workflow_2 = workflow_1.copy()
        workflow_2["name"] = "Automated test workflow 2"
        workflow_template_1 = WORKFLOW_TEMPLATE.copy()
        workflow_template_1["exam_id"] = postnewexamtemplate_response_json["id"]
        postworkflow_1_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_1, headers=headers, verify=False)
        assert postworkflow_1_response.status_code == 201
        postworkflow_1_response_json = postworkflow_1_response.json()
        postworkflow_2_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_2, headers=headers, verify=False)
        assert postworkflow_2_response.status_code == 201
        postworkflow_2_response_json = postworkflow_2_response.json()
        postworkflow_template_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_template_1, headers=headers, verify=False)
        assert postworkflow_template_response.status_code == 201
        postworkflow_template_response_json = postworkflow_template_response.json()
        task_1 = TASK_TEMPLATE.copy()
        task_1["workflow_id"] = postworkflow_1_response_json["id"]
        task_1["is_template"] = False
        task_2 = task_1.copy()
        task_2["name"] = "Automated test task 2"
        task_2["workflow_id"] = postworkflow_2_response_json["id"]
        task_template = task_1.copy()
        task_template["name"] = "Automated task template"
        task_template["workflow_id"] = postworkflow_template_response_json["id"]
        task_template["is_template"] = True
        posttask_1_response = requests.post(
            PREFIX + "/task/new", json=task_1, headers=headers, verify=False)
        assert posttask_1_response.status_code == 201
        posttask_1_response_json = posttask_1_response.json()
        posttask_2_response = requests.post(
            PREFIX + "/task/new", json=task_2, headers=headers, verify=False)
        assert posttask_1_response.status_code == 201
        posttask_2_response_json = posttask_2_response.json()
        posttask_template_response = requests.post(
            PREFIX + "/task/new", json=task_template, headers=headers, verify=False)
        assert posttask_template_response.status_code == 201
        posttask_template_response_json = posttask_template_response.json()

    # act
        deletetask_1_response = requests.delete(
            PREFIX + "/task/" + posttask_1_response_json["id"], 
            headers=headers, verify=False
        )
        deletetask_template_response = requests.delete(
            PREFIX + "/task/" + posttask_template_response_json["id"], 
            headers=headers, verify=False
        )

    # check
        assert deletetask_1_response.status_code == 204
        assert deletetask_template_response.status_code == 204
        gettask_1_response = requests.get(
            PREFIX + "/task/" + posttask_1_response_json["id"],
            headers=headers, verify=False)
        assert gettask_1_response.status_code == 404
        gettask_2_response = requests.get(
            PREFIX + "/task/" + posttask_2_response_json["id"],
            headers=headers, verify=False)
        assert gettask_2_response.status_code == 200
        gettasktemplate_response = requests.get(
            PREFIX + "/task/" + posttask_template_response_json["id"],
            headers=headers, verify=False)
        assert gettasktemplate_response.status_code == 404

    # act
        if postnewexam_response.status_code == 201:
            deleteexam_response = requests.delete(
                PREFIX + "/" + postnewexam_response_json["id"],
                headers=headers, verify=False
            )
        if postnewexamtemplate_response.status_code:
            deleteexamtemplate_presponse = requests.delete(
                PREFIX + "/" + postnewexamtemplate_response_json["id"],
                headers=headers, verify=False
            )

    # check
        assert deleteexam_response.status_code == 204
        assert deleteexamtemplate_presponse.status_code == 204
        gettask_2_response = requests.get(
            PREFIX + "/task/" + posttask_2_response_json["id"],
            headers=headers, verify=False)
        assert gettask_2_response.status_code == 404
        getworkflow_1_response = requests.get(
            PREFIX + "/workflow/" + postworkflow_1_response_json["id"],
            headers=headers, verify=False)
        assert getworkflow_1_response.status_code == 404
        getworkflow_2_response = requests.get(
            PREFIX + "/workflow/" + postworkflow_2_response_json["id"],
            headers=headers, verify=False)
        assert getworkflow_2_response.status_code == 404
        getexam_1_response = requests.get(
            PREFIX + "/exam/" + postnewexam_response_json["id"],
            headers=headers, verify=False)
        assert getexam_1_response.status_code == 404
        getexamtemplate_response = requests.get(
            PREFIX + "/exam/" + postnewexamtemplate_response_json["id"],
            headers=headers, verify=False)
        assert getexamtemplate_response.status_code == 404

    # cleanup
    finally:
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers, verify=False)
            assert deletepatient_1_response.status_code == 204


def test_update_task():
    # prepare
    access_token = login()
    headers = {"Authorization": "Bearer " + access_token}
    try:
        patient_1 = PATIENT.copy()
        postpatient_1_response = requests.post(
            PREFIX_PATIENT_MANAGER + "/", json=patient_1, headers=headers, verify=False)
        assert postpatient_1_response.status_code == 201
        postpatient_1_response_json = postpatient_1_response.json()
        exam_1 = EXAM_TEMPLATE.copy()
        exam_1["patient_id"] = postpatient_1_response_json["id"]
        exam_1["is_template"] = False
        postexam_1_response = requests.post(
            PREFIX + "/new", json=exam_1, headers=headers, verify=False)
        assert postexam_1_response.status_code == 201
        postexam_1_response_json = postexam_1_response.json()
        exam_2 = exam_1.copy()
        exam_2["name"] = "Automated test exam 2"
        postexam_2_response = requests.post(
            PREFIX + "/new", json=exam_2, headers=headers, verify=False)
        assert postexam_2_response.status_code == 201
        postexam_2_response_json = postexam_2_response.json()
        workflow_1 = WORKFLOW_TEMPLATE.copy()
        workflow_1["exam_id"] = postexam_1_response_json["id"]
        workflow_1["is_template"] = False
        workflow_2 = workflow_1.copy()
        workflow_2["name"] = "Automated test workflow 2"
        workflow_2["exam_id"] = postexam_2_response_json["id"]
        postworkflow_1_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_1, headers=headers, verify=False)
        assert postworkflow_1_response.status_code == 201
        postworkflow_1_response_json = postworkflow_1_response.json()
        postworkflow_2_response = requests.post(
            PREFIX + "/workflow/new", json=workflow_2, headers=headers, verify=False)
        assert postworkflow_2_response.status_code == 201
        postworkflow_2_response_json = postworkflow_2_response.json()
        task_1 = TASK_TEMPLATE.copy()
        task_1["workflow_id"] = postworkflow_1_response_json["id"]
        task_1["is_template"] = False
        posttask_1_response = requests.post(
            PREFIX + "/task/new", json=task_1, headers=headers, verify=False)
        assert posttask_1_response.status_code == 201
        posttask_1_response_json = posttask_1_response.json()
        update_request_1 = {
            "workflow_id": postworkflow_2_response_json["id"],
            "name": "Automated test task updated",
            "description": "some task description updated",
            "comment": "some test comment updated",
            "type": "RECONSTRUCTION_TASK",
            "args": {
                "arg1": "updated",
                "arg2 updated": "val2",
                "arg3 updated": "val3 updated"
            },
            "artifacts": {
                "some unspecified artifacts updated": "yay updated",
                # could enforce form of the values for input and output in the future
                "input": json.dumps([
                    {
                        "path": "/data updated",
                        "name": "inputfile2 updated"
                    }
                ]),
                "output": json.dumps([
                    {
                        "path": "/data updated",
                        "name": "outputfile1 updated"
                    }
                ])
            },
            "destinations": {
                "DICOM FANTASIA updated": "FANTASY PACS 1 updated",
                "RAWDATA FANTASIA updated": "FANTASY EXPORT INTERFACE 1"
            },
            "status": "FINISHED",
            "progress": 77,
            "is_template": False,
        }
        # update_request_2 = update_request_1.copy()
        # update_request_2["status"] = {"PENDING": "some status annotation"}
        update_request_3 = update_request_1.copy()
        update_request_3["workflow_id"] = "4969f66f-862e-4d4e-a6ff-a0a3fd1a14f5"
        update_request_4 = update_request_1.copy()
        update_request_4["is_template"] = True
        # TODO implement more conditions like in test_create_exam_from_template

    # act
        updatetask_response_1 = requests.put(
            PREFIX + "/task/" + posttask_1_response_json["id"],
            json=update_request_1,
            headers=headers, verify=False
        )

    # check
        assert updatetask_response_1.status_code == 200
        updatetask_response_1_json = updatetask_response_1.json()
        for key in update_request_1.keys():
            assert updatetask_response_1_json[key] == update_request_1[key]
        gettask_response_1 = requests.get(
            PREFIX + "/task/" + updatetask_response_1_json["id"],
            headers=headers, verify=False)
        assert gettask_response_1.status_code == 200
        gettask_response_1_json = gettask_response_1.json()
        for key in update_request_1.keys():
            if key != "status":
                assert gettask_response_1_json[key] == update_request_1[key]

    # # act
    #     updatetask_response_2 = requests.put(
    #         PREFIX + "/task/" + posttask_1_response_json["id"],
    #         json=update_request_2,
    #         headers=headers, verify=False
    #     )
    # # check
    #     assert updatetask_response_2.status_code == 403, \
    #         "Update status to PENDING should be rejected."  # debateble

    # act
        updatetask_response_3 = requests.put(
            PREFIX + "/task/" + posttask_1_response_json["id"],
            json=update_request_3,
            headers=headers, verify=False
        )
    # check
        assert updatetask_response_3.status_code == 400, \
            "Wrong workflow_id should be rejected."

    # act
        updatetask_response_4 = requests.put(
            PREFIX + "/task/" + posttask_1_response_json["id"],
            json=update_request_4,
            headers=headers, verify=False
        )
    # check
        assert updatetask_response_4.status_code == 400, \
            "Update to template with reference to workflow instance should be rejected."

    # cleanup
    finally:
        if postexam_1_response.status_code == 201:
            deleteexam_1_response = requests.delete(
                PREFIX + "/" + 
                postexam_1_response_json["id"],
                headers=headers, verify=False)
            assert deleteexam_1_response.status_code == 204
        if postexam_2_response.status_code == 201:
            deleteexam_2_response = requests.delete(
                PREFIX + "/" + 
                postexam_2_response_json["id"],
                headers=headers, verify=False)
            assert deleteexam_2_response.status_code == 204
        if postpatient_1_response.status_code == 201:
            deletepatient_1_response = requests.delete(
                PREFIX_PATIENT_MANAGER + "/" + 
                str(postpatient_1_response_json["id"]),
                headers=headers, verify=False)
            assert deletepatient_1_response.status_code == 204