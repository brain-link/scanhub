# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of exam API endpoints accessible through swagger UI."""

from typing import Annotated
from uuid import UUID

import requests
from fastapi import APIRouter, Depends, HTTPException
from scanhub_libraries.models import BaseExam, ExamOut, ItemStatus, User
from scanhub_libraries.security import get_current_user, oauth2_scheme

from app import LOG_CALL_DELIMITER
from app.api import workflow_api
from app.dal import exam_dal

# from app.workflow_api import create_workflow_from_template
# from app.db import Exam, Workflow
from app.tools.helper import get_exam_out_model

# Http status codes
# 200 = Ok: GET, PUT
# 201 = Created: POST
# 204 = No Content: Delete
# 404 = Not found

PREFIX_PATIENT_MANAGER = "http://patient-manager:8100/api/v1/patient"
# PREFIX_PATIENT_MANAGER = "http://host.docker.internal:8090/api/v1/patient"

exam_router = APIRouter(dependencies=[Depends(get_current_user)])


@exam_router.post("/new", response_model=ExamOut, status_code=201, tags=["exams"])
async def create_exam(
    payload: BaseExam,
    user: Annotated[User, Depends(get_current_user)],
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> ExamOut:
    """Create a new exam.

    Parameters
    ----------
    payload
        Exam pydantic input model.

    Returns
    -------
        Exam pydantic output moddel.

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("Payload:", payload)
    if payload.status != "NEW":
        raise HTTPException(status_code=400, detail="New exam needs to have status NEW.")
    if payload.is_template is False:
        if payload.patient_id is None:
            raise HTTPException(status_code=400, detail="patient_id must be given to create exam.")
        getpatient_response = requests.get(
            PREFIX_PATIENT_MANAGER + "/" + str(payload.patient_id),
            headers={"Authorization": "Bearer " + access_token},
            timeout=3,
        )

        if getpatient_response.status_code != 200:
            raise HTTPException(status_code=400, detail="patient_id must refer to an existing patient.")
    if payload.is_template is True and payload.patient_id is not None:
        raise HTTPException(status_code=400, detail="Exam template must not have patient_id.")
    if not (exam := await exam_dal.add_exam_data(payload=payload, creator=user.username)):
        raise HTTPException(status_code=404, detail="Could not create exam")
    return await get_exam_out_model(data=exam)


@exam_router.post("/", response_model=ExamOut, status_code=201, tags=["exams"])
async def create_exam_from_template(
    payload: BaseExam,
    template_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> ExamOut:
    """Create a new exam from template.

    Parameters
    ----------
    payload
        The potentially modified exam to create.
    template_id
        ID of the template, the exam is created from

    Returns
    -------
        Exam pydantic output model.

    Raises
    ------
    HTTPException
        404: Creation unsuccessful
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("Exam:", payload)
    print("template_id:", template_id)
    if payload.is_template is False:
        if payload.patient_id is None:
            raise HTTPException(status_code=400, detail="patient_id must be given to create exam instance.")
        getpatient_response = requests.get(
            PREFIX_PATIENT_MANAGER + "/" + str(payload.patient_id),
            headers={"Authorization": "Bearer " + access_token},
            timeout=3,
        )
        print("getpatient_response: ", getpatient_response)
        print("url: ", PREFIX_PATIENT_MANAGER + "/" + str(payload.patient_id))
        if getpatient_response.status_code != 200:
            raise HTTPException(status_code=400, detail="patient_id must refer to an existing patient.")
    if payload.is_template is True and payload.patient_id is not None:
        raise HTTPException(status_code=400, detail="Exam template must not have patient_id.")
    if not (template := await exam_dal.get_exam_data(exam_id=template_id)):
        raise HTTPException(status_code=400, detail="Template not found.")
    if template.is_template is not True:
        raise HTTPException(
            status_code=400, detail="Request to create exam from exam instance instead of exam template."
        )
    new_exam = BaseExam(**payload.__dict__)
    new_exam.status = ItemStatus.NEW
    if not (exam := await exam_dal.add_exam_data(payload=new_exam, creator=user.username)):
        raise HTTPException(status_code=404, detail="Could not create exam.")

    exam_out = await get_exam_out_model(data=exam)

    # Create all the sub-items for the workflow templates in the exam template
    for workflow in template.workflows:
        exam_out.workflows.append(
            await workflow_api.create_workflow_from_template(
                exam_id=exam.id, template_id=workflow.id, new_workflow_is_template=exam.is_template, user=user
            )
        )
    return exam_out


@exam_router.get("/{exam_id}", response_model=ExamOut, status_code=200, tags=["exams"])
async def get_exam(exam_id: UUID | str, user: Annotated[User, Depends(get_current_user)]) -> ExamOut:
    """Get exam endpoint.

    Parameters
    ----------
    exam_id
        Id of requested exam entry

    Returns
    -------
        Exam pydantic output model.

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("exam_id:", exam_id)
    try:
        _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    except ValueError:
        raise HTTPException(status_code=400, detail="Badly formed exam_id")
    if not (exam := await exam_dal.get_exam_data(exam_id=_id)):
        raise HTTPException(status_code=404, detail="Exam not found")
    return await get_exam_out_model(data=exam)


@exam_router.get("/all/{patient_id}", response_model=list[ExamOut], status_code=200, tags=["exams"])
async def get_all_patient_exams(patient_id: UUID, user: Annotated[User, Depends(get_current_user)]) -> list[ExamOut]:
    """Get all exams of a certain patient.

    Parameters
    ----------
    patient_id
        Id of parent

    Returns
    -------
        List of exam pydantic output models
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("Getting exams for patient_id:", patient_id)
    if not (exams := await exam_dal.get_all_exam_data(patient_id=patient_id)):
        # Don't raise exception here, list might be empty
        return []
    result = [await get_exam_out_model(data=exam) for exam in exams]
    return result


@exam_router.get("/templates/all", response_model=list[ExamOut], status_code=200, tags=["exams"])
async def get_all_exam_templates(user: Annotated[User, Depends(get_current_user)]) -> list[ExamOut]:
    """Get all exam templates.

    Returns
    -------
        List of exam pydantic output models
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    if not (exams := await exam_dal.get_all_exam_template_data()):
        # Don't raise exception here, list might be empty
        return []
    result = [await get_exam_out_model(data=exam) for exam in exams]
    print("Number of exam templates: ", len(result))
    return result


@exam_router.delete("/{exam_id}", response_model={}, status_code=204, tags=["exams"])
async def exam_delete(exam_id: UUID | str, user: Annotated[User, Depends(get_current_user)]) -> None:
    """Delete an exam by id. Cascade deletes the associated workflow and tasks.

    Parameters
    ----------
    exam_id
        Id of the exam to be deleted

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("exam_id:", exam_id)
    _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    if not await exam_dal.delete_exam_data(exam_id=_id):
        message = "Could not delete exam, either because it does not exist, or for another reason."
        raise HTTPException(status_code=404, detail=message)


@exam_router.put("/{exam_id}", response_model=ExamOut, status_code=200, tags=["exams"])
async def update_exam(
    exam_id: UUID | str,
    payload: BaseExam,
    user: Annotated[User, Depends(get_current_user)],
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> ExamOut:
    """Update an existing exam.

    Parameters
    ----------
    exam_id
        Id of the exam to be updated
    payload
        Exam pydantic input model

    Returns
    -------
        Exam pydantic output model

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("exam_id:", exam_id)
    if payload.is_template is False:
        if payload.patient_id is None:
            raise HTTPException(status_code=400, detail="patient_id must be given for exam instance.")
        getpatient_response = requests.get(
            PREFIX_PATIENT_MANAGER + "/" + str(payload.patient_id),
            headers={"Authorization": "Bearer " + access_token},
            timeout=3,
        )
        if getpatient_response.status_code != 200:
            raise HTTPException(status_code=400, detail="patient_id must refer to an existing patient.")
        # for now, allow changing the patient_id, but could require administrator rights in the future
    if payload.is_template is True and payload.patient_id is not None:
        raise HTTPException(status_code=400, detail="Exam template must not have patient_id.")
    # for now allow changing is_template in principle, but that could be refused in the future
    if payload.status == "NEW":
        raise HTTPException(status_code=403, detail="Exam cannot be updated to status NEW.")
    _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    if not (exam_updated := await exam_dal.update_exam_data(exam_id=_id, payload=payload)):
        message = "Could not update exam, either because it does not exist, or for another reason."
        raise HTTPException(status_code=404, detail=message)
    return await get_exam_out_model(data=exam_updated)
