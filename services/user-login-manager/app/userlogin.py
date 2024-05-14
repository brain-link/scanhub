# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of the user management and login API endpoints (accessible through swagger UI)."""

from typing import Annotated
from hashlib import sha256, scrypt
from secrets import compare_digest, token_hex
from passlib.hash import argon2
import time

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from scanhub_libraries.models import User

from app import dal
# TODO check need for these files: from app.db import Exam, Workflow


router = APIRouter()



def compute_complex_password_hash(password: str, salt: str) -> str:
    """ 
        Function to compute a complex password hash with salt. 
        It should take quite a bit of computation to guard against brute force attacks. 
    """
    start_time = time.time()
    password_plain_hash = sha256(bytes(password, 'utf8')).hexdigest()               # plain sha256 hash from python standard library (not enough for brute force attack)
    password_scrypt_hash = scrypt(password=bytes(password_plain_hash, 'utf8'), 
                                  salt=bytes(salt, 'utf8'),
                                  n=256, r=128, p=32)                               # scrypt from python standard library function (designed for password digestion)
    password_argon2_hash = argon2.using(salt=bytes(salt, 'utf8')).hash(secret=password_scrypt_hash)    # argon2 from passlib (recommended memory intensive password digest, current year is 2024)
    password_final_hash = sha256(bytes(password_argon2_hash, 'utf-8')).hexdigest()      # another round of plain sha256 from python standard library, why not
    if (time.time() - start_time < 0.1):
        print("WARNING: compute_complex_password_hash is faster than 0.1 sec, consider increasing the parameters to ensure security of password hashes.")
    return password_final_hash


@router.post("/login", tags=["login"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> User:
    """Login endpoint.

    Parameters
    ----------
    form_data
        Http form data for OAuth2 compliant login with username and password.

    Returns
    -------
        User pydantic model, the user data in case of a successful login.

    Raises
    ------
    HTTPException
        401: Unauthorized if the username or password is wrong.
    """
    user_db = await dal.get_user_data(form_data.username)
    if user_db == None:
        print("Login try by unknown user. Username:", form_data.username)
        dummy_hash = compute_complex_password_hash(form_data.password, token_hex(1024))     # avoid timing attack
        compare_digest(dummy_hash, dummy_hash)                                              # avoid timing attack
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})
    else:
        hashed_received_password = compute_complex_password_hash(form_data.password, user_db.salt)
        password_hash_matches = compare_digest(hashed_received_password, user_db.password_hash)
        if not password_hash_matches:
            print("Login try with wrong password. Username:", form_data.username)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"})
        elif user_db.token is not None and time.time() - user_db.last_activity_unixtime < 60 * 60:  # auto-logout time 1 hour
            # user still logged in, return the current token
            print("Login while user is already logged in. Username:", form_data.username)
            await dal.update_user_data(form_data.username, {"last_activity_unixtime": time.time()})
            return User(
                username=user_db.username, 
                first_name=user_db.first_name, 
                last_name=user_db.last_name, 
                email=user_db.email,
                token=user_db.token, 
                token_type="bearer"
            )
        else:
            # user not logged in anymore, create new token
            print("Login. Username:", form_data.username)
            newtoken = token_hex(256)
            await dal.update_user_data(form_data.username, {"token": newtoken, "last_activity_unixtime": time.time()})
            return User(
                username=user_db.username, 
                first_name=user_db.first_name, 
                last_name=user_db.last_name, 
                email=user_db.email,
                token=newtoken, 
                token_type="bearer"
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