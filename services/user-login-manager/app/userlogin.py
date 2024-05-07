# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of the user management and login API endpoints (accessible through swagger UI)."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
# TODO check need for these files: from scanhub_libraries.models import BaseExam, BaseTask, BaseWorkflow, ExamOut, TaskOut, WorkflowOut

# TODO check need for these files: from app import dal
# TODO check need for these files: from app.db import Exam, Workflow


router = APIRouter()


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    print("Call to login with username:", form_data.username, "and password:", form_data.password)
    print("TODO: implement login. For now return token 'Bitte'.")
    return {"access_token": "Bitte", "token_type": "bearer"}