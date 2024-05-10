# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of the user management and login API endpoints (accessible through swagger UI)."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from scanhub_libraries.models import User, UserOut

# TODO check need for these files: from app import dal
# TODO check need for these files: from app.db import Exam, Workflow


router = APIRouter()


@router.post("/login", tags=["login"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> UserOut:
    print("Call to login with username:", form_data.username, "and password:", form_data.password)
    print("TODO: implement login. For now return token 'Bitte'.")
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


