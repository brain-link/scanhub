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
from scanhub_libraries.db import UserSQL
from scanhub_libraries.security import AUTOMATIC_LOGOUT_TIME_SECONDS, get_current_user
from scanhub_libraries import dal


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
        elif user_db.access_token is not None and time.time() - user_db.last_activity_unixtime < AUTOMATIC_LOGOUT_TIME_SECONDS:  # auto-logout time 1 hour
            # user still logged in, return the current token
            print("Login while user is already logged in. Username:", form_data.username)
            await dal.update_user_data(form_data.username, {"last_activity_unixtime": time.time()})
            return User(
                username=user_db.username, 
                first_name=user_db.first_name, 
                last_name=user_db.last_name, 
                email=user_db.email,
                access_token=user_db.access_token, 
                token_type="bearer"
            )
        else:
            # user not logged in anymore, create new token
            print("Login. Username:", form_data.username)
            newtoken = token_hex(256)
            await dal.update_user_data(form_data.username, {"access_token": newtoken, "last_activity_unixtime": time.time()})
            return User(
                username=user_db.username, 
                first_name=user_db.first_name, 
                last_name=user_db.last_name, 
                email=user_db.email,
                access_token=newtoken, 
                token_type="bearer"
            )


@router.post("/logout", tags=["login"])
async def login(user: Annotated[UserSQL, Depends(get_current_user)]) -> None:
    """
    Logout endpoint.
    """
    print("Logout. Username:", user.username)
    await dal.update_user_data(user.username, {"access_token": None, "last_activity_unixtime": time.time()})