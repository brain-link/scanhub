# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of the user management and login API endpoints (accessible through swagger UI)."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from scanhub_libraries.models import User, UserOut

# TODO check need for these files: from app import dal
# TODO check need for these files: from app.db import Exam, Workflow


router = APIRouter()


@router.post("/login", tags=["login"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> UserOut:
    print("Call to login with username:", form_data.username, "and password:", form_data.password)
    print("TODO: implement login.")
    if (form_data.username != "Max" or form_data.password != "letmein"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})
    return UserOut(
        access_token="Bitte", 
        token_type="bearer", 
        user=User(
            username="maxi123", 
            first_name="Maximiliane", 
            last_name="Musterfrau", 
            email="maxi123mail@mail.de"
        )
    )





# # Helper methods for workflows and exam, require recursive model translation
# async def get_workflow_out_model(data: Workflow) -> WorkflowOut:
#     """Transform db model to pydantic model.

#     Parameters
#     ----------
#     data
#         Workflow db model

#     Returns
#     -------
#         Workflow pydantic model
#     """
#     workflow = data.__dict__
#     workflow["tasks"] = [TaskOut(**task.__dict__) for task in data.tasks]
#     return WorkflowOut(**workflow)


# async def get_exam_out_model(data: Exam) -> ExamOut:
#     """Transform db model to pydantic model.

#     Parameters
#     ----------
#     data
#         Exam db model

#     Returns
#     -------
#         Exam pydantic model
#     """
#     exam = data.__dict__
#     exam["workflows"] = [await get_workflow_out_model(workflow) for workflow in data.workflows]
#     return ExamOut(**exam)




# @router.post("/", response_model=ExamOut, status_code=201, tags=["exams"])
# async def create_exam_from_template(patient_id: int, template_id: UUID) -> ExamOut:
#     """Create a new exam instance from template.

#     Parameters
#     ----------
#     patient_id
#         Id of the patient, the exam instance is related to
#     template_id
#         ID of the template, the exam is created from

#     Returns
#     -------
#         Exam pydantic output moddel.

#     Raises
#     ------
#     HTTPException
#         404: Creation unsuccessful
#     """
#     template = await get_exam(exam_id=template_id)
#     instance = BaseExam(**template.__dict__)
#     instance.is_template = False
#     instance.patient_id = patient_id
#     if not (exam := await dal.add_exam_data(payload=instance)):
#         raise HTTPException(status_code=404, detail="Could not create exam instance")
#     return await get_exam_out_model(data=exam)


# @router.put("/{exam_id}", response_model=ExamOut, status_code=200, tags=["exams"])
# async def update_exam(exam_id: UUID | str, payload: BaseExam) -> ExamOut:
#     """Update an existing exam.

#     Parameters
#     ----------
#     exam_id
#         Id of the exam to be updated
#     payload
#         Exam pydantic input model

#     Returns
#     -------
#         Exam pydantic output model

#     Raises
#     ------
#     HTTPException
#         404: Not found
#     """
#     _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
#     exam = await get_exam(exam_id=_id)
#     if exam.is_frozen:
#         raise HTTPException(status_code=404, detail="Exam is frozen an cannot be edited.")
#     if not (exam_updated := await dal.update_exam_data(exam_id=_id, payload=payload)):
#         raise HTTPException(status_code=404, detail="Exam not found")
#     return await get_exam_out_model(data=exam_updated)


# @router.get("/{exam_id}", response_model=ExamOut, status_code=200, tags=["exams"])
# async def get_exam(exam_id: UUID | str) -> ExamOut:
#     """Get exam endpoint.

#     Parameters
#     ----------
#     exam_id
#         Id of requested exam entry

#     Returns
#     -------
#         Exam pydantic output model.

#     Raises
#     ------
#     HTTPException
#         404: Not found
#     """
#     _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
#     if not (exam := await dal.get_exam_data(exam_id=_id)):
#         raise HTTPException(status_code=404, detail="Exam not found")
#     return await get_exam_out_model(data=exam)


# @router.delete("/{exam_id}", response_model={}, status_code=204, tags=["exams"])
# async def exam_delete(exam_id: UUID | str) -> None:
#     """Delete an existing exam by id.

#     Parameters
#     ----------
#     exam_id
#         Id of the exam to be deleted

#     Raises
#     ------
#     HTTPException
#         404: Not found
#     """
#     _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
#     exam = await get_exam(exam_id=_id)
#     if exam.is_frozen:
#         raise HTTPException(status_code=404, detail="Exam is frozen and cannot be deleted.")
#     if not await dal.delete_exam_data(exam_id=_id):
#         raise HTTPException(status_code=404, detail="Exam not found")


# @router.get("/all/{patient_id}", response_model=list[ExamOut], status_code=200, tags=["exams"])
# async def get_all_patient_exams(patient_id: int) -> list[ExamOut]:
#     """Get all exams of a certain patient.

#     Parameters
#     ----------
#     patient_id
#         Id of parent

#     Returns
#     -------
#         List of exam pydantic output models
#     """
#     if not (exams := await dal.get_all_exam_data(patient_id=patient_id)):
#         # Don't raise exception here, list might be empty
#         return []
#     result = [await get_exam_out_model(data=exam) for exam in exams]
#     print(">> Exam list: ", result)
#     return result