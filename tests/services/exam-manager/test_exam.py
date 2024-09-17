# Copyright (C) 2024.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

""" pytest tests for exam.py """

import requests
# import sys
# sys.path.append("../../../services/exam-manager/app/")
# import dal



PREFIX = "http://localhost:8080/api/v1/exam"
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


def test_wrong_token():
    login()
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
    response = requests.post(PREFIX + "/new",
                        json=exam,
                        headers={"Authorization": "Bearer " + "wrongaccesstoken"},
                        timeout=3)
    assert response.status_code == 401


def test_no_token():
    login()
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
    response = requests.post(PREFIX + "/new", json=exam)
    assert response.status_code == 401


def test_create_exam():
    # prepare
    access_token = login()

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
    postexam_response = requests.post(
        PREFIX + "/new",
        json=exam,
        headers={"Authorization": "Bearer " + access_token})
    assert postexam_response.status_code == 201

    # check
    try:
        postexam_response_json = postexam_response.json()
        for key in exam.keys():
            assert postexam_response_json[key] == exam[key]
        getexam_response = requests.get(
            PREFIX + "/" + postexam_response_json["id"],
            headers={"Authorization": "Bearer " + access_token})
        assert getexam_response.status_code == 200
        getexam_response_json = getexam_response.json()
        for key in exam.keys():
            assert getexam_response_json[key] == exam[key]

    # cleanup
    finally:
        deleteexam_response = requests.delete(
            PREFIX + "/" + 
            postexam_response_json["id"],
            headers={"Authorization": "Bearer " + access_token})
        assert deleteexam_response.status_code == 204


def test_create_exam_from_template():
    # prepare
    access_token = login()
    exam_template = {
        "name": "test_exam_template",
        "country": "blablastan",
        "site": "middle of nowhere",
        "address": "midway",
        "creator": "Max",
        "status": "NEW",
        "is_template": True,
        "is_frozen": False
    }
    try:
        postnewtemplate_response = requests.post(
            PREFIX + "/new",
            json=exam_template,
            headers={"Authorization": "Bearer " + access_token})
        assert postnewtemplate_response.status_code == 201
        postnewtemplate_response_json = postnewtemplate_response.json()

    # act
        postexamfromtemplate_response = requests.post(
            PREFIX + "/",
            params={
                "patient_id": 123, 
                "template_id": postnewtemplate_response_json["id"],
                "new_exam_is_template": False
            },
            headers={"Authorization": "Bearer " + access_token})

    # check
        assert postexamfromtemplate_response.status_code == 201
        postexamfromtemplate_response_json = postexamfromtemplate_response.json()
        for key in exam_template.keys():
            if key != "is_template":
                assert postexamfromtemplate_response_json[key] == exam_template[key]
        assert postexamfromtemplate_response_json["patient_id"] == 123
        assert postexamfromtemplate_response_json["is_template"] is False
        getexam_response = requests.get(
            PREFIX + "/" + postexamfromtemplate_response_json["id"],
            headers={"Authorization": "Bearer " + access_token})
        assert getexam_response.status_code == 200
        getexam_response_json = getexam_response.json()
        for key in exam_template.keys():
            if key != "is_template":
                assert getexam_response_json[key] == exam_template[key]
        assert getexam_response_json["patient_id"] == 123
        assert getexam_response_json["is_template"] is False

    # cleanup
    finally:
        if postnewtemplate_response.status_code == 201:
            deleteexamtemplate_response = requests.delete(
                PREFIX + "/" + postnewtemplate_response_json["id"],
                headers={"Authorization": "Bearer " + access_token})
            assert deleteexamtemplate_response.status_code == 204
        if postexamfromtemplate_response.status_code == 201:
            deleteexam_response = requests.delete(
                PREFIX + "/" + postexamfromtemplate_response_json["id"],
                headers={"Authorization": "Bearer " + access_token})
            assert deleteexam_response.status_code == 204


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
    exam1 = {
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
    try:
        exam2 = exam1.copy()
        exam2["site"] = "test site 2"
        exam3 = exam1.copy()
        exam3["site"] = "test site 3"
        exam3["patient_id"] = 456
        postnewexam1_response = requests.post(
            PREFIX + "/new",
            json=exam1,
            headers={"Authorization": "Bearer " + access_token}
        )
        postnewexam2_response = requests.post(
            PREFIX + "/new",
            json=exam2,
            headers={"Authorization": "Bearer " + access_token}
        )
        postnewexam3_response = requests.post(
            PREFIX + "/new",
            json=exam3,
            headers={"Authorization": "Bearer " + access_token}
        )
        assert postnewexam1_response.status_code == 201
        assert postnewexam2_response.status_code == 201
        assert postnewexam3_response.status_code == 201

    # act
        getallexams_response = requests.get(
            PREFIX + "/all/123",
            headers={"Authorization": "Bearer " + access_token})

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
                PREFIX + "/" + postnewexam1_response.json()["id"],
                headers={"Authorization": "Bearer " + access_token}
            )
            assert deleteexam1_response.status_code == 204
        if postnewexam2_response.status_code == 201:
            deleteexam2_response = requests.delete(
                PREFIX + "/" + postnewexam2_response.json()["id"],
                headers={"Authorization": "Bearer " + access_token}
            )
            assert deleteexam2_response.status_code == 204
        if postnewexam3_response.status_code == 201:
            deleteexam3_response = requests.delete(
                PREFIX + "/" + postnewexam3_response.json()["id"],
                headers={"Authorization": "Bearer " + access_token}
            )
            assert deleteexam3_response.status_code == 204


def test_get_all_exam_templates():
    # prepare
    access_token = login()
    exam_template_1 = {
        "name": "test_exam_template",
        "country": "blablastan",
        "site": "middle of nowhere",
        "address": "midway",
        "creator": "Max",
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

    exam = {
        "patient_id": 777,
        "name": "test_exam",
        "country": "blablastan",
        "site": "middle of nowhere",
        "address": "midway",
        "creator": "Max",
        "status": "NEW",
        "is_template": False,
        "is_frozen": False
    }
    postnewexam_response = requests.post(
        PREFIX + "/new",
        json=exam,
        headers={"Authorization": "Bearer " + access_token}
    )
    assert postnewexam_response.status_code == 201
    postnewexam_response_json = postnewexam_response.json()
    deleteexam_response = requests.delete(
        PREFIX + "/" + postnewexam_response_json["id"],
        headers={"Authorization": "Bearer " + access_token}
    )
    assert deleteexam_response.status_code == 204

    exam_template = {
        "name": "test_exam_template",
        "country": "blablastan",
        "site": "middle of nowhere",
        "address": "midway",
        "creator": "Max",
        "status": "NEW",
        "is_template": True,
        "is_frozen": False
    }
    postnewtemplate_response = requests.post(
        PREFIX + "/new",
        json=exam_template,
        headers={"Authorization": "Bearer " + access_token})
    assert postnewtemplate_response.status_code == 201
    postnewtemplate_response_json = postnewtemplate_response.json()
    deleteexamtemplate_presponse = requests.delete(
        PREFIX + "/" + postnewtemplate_response_json["id"],
        headers={"Authorization": "Bearer " + access_token},
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
        headers={"Authorization": "Bearer " + access_token})
    assert getexam_response.status_code == 404
    getexamtemplate_response = requests.get(
        PREFIX + "/" + postnewtemplate_response_json["id"],
        headers={"Authorization": "Bearer " + access_token})
    assert getexamtemplate_response.status_code == 404

    # postnewexamfrozen_response_json = postnewexamfrozen_response.json()
    # deleteexamfrozen_response = requests.delete(
    #     PREFIX + "/" + postnewexamfrozen_response_json["id"],
    #     headers={"Authorization": "Bearer " + access_token}
    # )
    # assert deleteexamfrozen_response.status_code == 404

    # cleanup (only necessary for the frozen item)
    # TODO implement cleanup of frozen item


# TODO test if items are created/deleted recursively (exam->workflows->tasks)
# e.g. test for create_exam_from_template if associated workflows are generated