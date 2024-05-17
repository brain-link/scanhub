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


async def get_user_out(user_db: UserSQL):
    """ Convert UserSQL to User, replace token with empty string. """
    # UserSQL
    # --------
    # username: Mapped[str] = mapped_column(primary_key=True)
    # first_name: Mapped[str] = mapped_column(nullable=False)
    # last_name: Mapped[str] = mapped_column(nullable=False)
    # email: Mapped[str] = mapped_column(nullable=False)
    # password_hash: Mapped[str] = mapped_column(nullable=False)
    # salt: Mapped[str] = mapped_column(nullable=False)               # salt used to create the password_hash
    # access_token: Mapped[str] = mapped_column(nullable=True, unique=True)          # token used to access backend while user is logged in, None if user is logged out
    # last_activity_unixtime: Mapped[int] = mapped_column(nullable=True)      # time of last activity, used for automatic logout

    # User
    # ---------
    # username: str
    # first_name: str
    # last_name: str
    # email: str | None
    # access_token: str   # access_token and token_type are standardized names in OAuth2, don't change them
    # token_type: str     # token_type should always be "bearer" as standardized in OAuth2
    return User(
        username=user_db.username,
        first_name=user_db.first_name,
        last_name=user_db.last_name,
        email=user_db.email,
        access_token="",        # TODO could be removed here, would need to change the pydantic model
        token_type=""           # TODO could be removed here, would need to change the pydantic model
    )


@router.get('/getallusers', response_model=list[User], status_code=200, tags=["user"])
async def get_user_list(current_user: Annotated[UserSQL, Depends(get_current_user)]) -> list[User]:
    """Get all users endpoint.

    Returns
    -------
        List of all users. The access_token and token_type properties are set to "" for all of them.
    """
    users: list[UserSQL] = await dal.get_all_users()
    if not (users):
        # If return is none, list is empty
        return []
    return [await get_user_out(user) for user in users]


@router.post("/createuser", status_code=201, tags=["user"])
async def create_user(current_user: Annotated[UserSQL, Depends(get_current_user)], new_user: User):
    """Create new patient database entry.

    Parameters
    ----------
    new_user
        pydantic base model of new user, token_type should be "password" and access_token should contain the password of the new user.
        The password of the new user should at least be 12 characters long.

    Returns
    -------
        Patient pydantic output model

    """
    user_db = await dal.get_user_data(new_user.username)
    if user_db is not None:
        print("Requested to create user that already exists.")
        raise HTTPException(
            status_code=500,
            detail="User already exists.")
    if new_user.token_type != "password":
        raise HTTPException(
            status_code=400,
            detail="To create a new user, the token_type should be 'password'!")
    if len(new_user.access_token) < 12:
        raise HTTPException(
            status_code=400,
            detail="The password should at least be 12 characters long!")
    print("Create new user! Username:", new_user.username)
    salt = token_hex(1024)  # create new salt
    hashed_received_password = compute_complex_password_hash(new_user.access_token, salt)
    new_user_db = UserSQL(
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        password_hash=hashed_received_password,
        salt=salt,
        access_token=None,
        last_activity_unixtime=None
    )
    await dal.add_user(new_user_db)
