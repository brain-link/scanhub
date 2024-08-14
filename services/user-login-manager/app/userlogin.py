# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of the user management and login API endpoints (accessible through swagger UI)."""

import time
from hashlib import scrypt, sha256
from secrets import compare_digest, token_hex
from typing import Annotated, Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import argon2
from scanhub_libraries.models import User, UserRole
from scanhub_libraries.security import oauth2_scheme

from app import dal
from app.db import UserSQL

AUTOMATIC_LOGOUT_TIME_SECONDS = 3600    # time without activity until login token gets invalid
FORCED_LOGOUT_TIME_SECONDS = 3600 * 11  # time until forced logout, independent of activity


router = APIRouter()


@router.get("/getcurrentuser", status_code=200, tags=["user"])
async def get_current_user(access_token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """
    Get current user from access_token. May be called as an endpoint or used in FastAPI with Depends.

    Parameters
    ----------
    access_token
        User token as previously obtained trough a call to /login
        Submit via HTTP header "Authorization: Bearer <access_token>"

    Returns
    -------
        User pydantic model, the user data of the current user.

    Raises
    ------
    HTTPException
        401: Unauthorized if the token is invalid or outdated.
    """
    user_db: UserSQL | None = await dal.get_user_from_token(access_token)
    if  (       user_db is not None
            and user_db.access_token is not None
            and user_db.last_activity_unixtime is not None
            and time.time() - user_db.last_activity_unixtime < AUTOMATIC_LOGOUT_TIME_SECONDS
            and user_db.last_login_unixtime is not None
            and time.time() - user_db.last_login_unixtime < FORCED_LOGOUT_TIME_SECONDS):
        # reset last_activity timer
        await dal.update_user_data(user_db.username, {"last_activity_unixtime": time.time()})
        user = await get_user_out(user_db)
        return user

    print("Received invalid token.")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token.",
        headers={"WWW-Authenticate": "Bearer"},
    )


# @router.get("/getcurrentuseradmin", status_code=200, tags=["user"])
async def get_current_user_admin(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """
    Check if the current_user has the role admin. May be (called as an endpoint or) used in FastAPI with Depends.

    Parameters
    ----------
    current_user
        The current_user as determined by get_current_user from the access_token.
        Submit the access_token via HTTP header "Authorization: Bearer <access_token>"

    Returns
    -------
        User pydantic model, the user data of the current user, who needs to have the role admin.

    Raises
    ------
    HTTPException
        401: Unauthorized if the token is invalid or user is not admin.
    """
    if current_user.role == UserRole.admin:
        return current_user

    print("User is not admin.")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User is not admin.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def compute_complex_password_hash(password: str, salt: str) -> str:
    """
    Compute a complex password hash with salt.

    It should take quite a bit of computation to guard against brute force attacks.
    """
    start_time = time.time()
    # plain sha256 hash from python standard library (not enough for brute force attack)
    password_plain_hash = sha256(bytes(password, 'utf8')).hexdigest()
    # scrypt from python standard library function (designed for password digestion)
    password_scrypt_hash = scrypt(password=bytes(password_plain_hash, 'utf8'),
                                  salt=bytes(salt, 'utf8'),
                                  n=256, r=128, p=32)
    # argon2 from passlib (recommended memory intensive password digest, current year is 2024)
    password_argon2_hash = argon2.using(salt=bytes(salt, 'utf8')).hash(secret=password_scrypt_hash)
    # another round of plain sha256 from python standard library, why not
    password_final_hash = sha256(bytes(password_argon2_hash, 'utf-8')).hexdigest()
    if (time.time() - start_time < 0.1):
        print("WARNING: compute_complex_password_hash is faster than 0.1 sec, \
              consider increasing the parameters to ensure security of password hashes.")
    return password_final_hash



@router.post("/loginfromcookie", tags=["login"])
async def loginfromcookie(response: Response, access_token: Annotated[Optional[str], Cookie()] = None) -> User:
    """Login endpoint for login with cookie.

    Parameters
    ----------
    access_token
        User token as previously obtained trough a call to /login
        Submit via HTTP cookie.

    Returns
    -------
        User pydantic model, the user data in case of a successful login.

    Raises
    ------
    HTTPException
        401: Unauthorized if the username or password is wrong.
    """
    if access_token is None:
        print("Missing token.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # raises error if access_token is invalid, resets last activity time
    current_user = await get_current_user(access_token)

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=max(AUTOMATIC_LOGOUT_TIME_SECONDS, FORCED_LOGOUT_TIME_SECONDS),
        path="/api/v1/userlogin/loginfromcookie",
        secure=True,
        httponly=True,
        samesite='strict'
    )
    return User(
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        role=current_user.role,
        access_token=access_token,
        token_type="bearer",    # noqa: S106
        last_activity_unixtime=None,
        last_login_unixtime=None
    )


@router.post("/login", tags=["login"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response) -> User:
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
    if user_db is None:
        print("Login try by unknown user. Username:", form_data.username)
        dummy_hash = compute_complex_password_hash(form_data.password, token_hex(1024))     # avoid timing attack
        compare_digest(dummy_hash, dummy_hash)                                              # avoid timing attack
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})

    hashed_received_password = compute_complex_password_hash(form_data.password, user_db.salt)
    password_hash_matches = compare_digest(hashed_received_password, user_db.password_hash)
    if not password_hash_matches:
        print("Login try with wrong password. Username:", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})

    if (        user_db.access_token is not None
            and user_db.last_activity_unixtime is not None
            and time.time() - user_db.last_activity_unixtime < AUTOMATIC_LOGOUT_TIME_SECONDS
            and user_db.last_login_unixtime is not None
            and time.time() - user_db.last_login_unixtime < FORCED_LOGOUT_TIME_SECONDS):
        # user still logged in, return the current token
        print("Login while user is already logged in. Username:", form_data.username)
        await dal.update_user_data(form_data.username, {"last_activity_unixtime": time.time()})
        return_token = user_db.access_token
    else:
        # user not logged in anymore, create new token
        print("Login. Username:", form_data.username)
        newtoken = token_hex(256)
        now = time.time()
        await dal.update_user_data(
            form_data.username,
            {
                "access_token": newtoken,
                "last_activity_unixtime": now,
                "last_login_unixtime": now
            }
        )
        return_token = newtoken
    response.set_cookie(
        key="access_token",
        value=return_token,
        max_age=max(AUTOMATIC_LOGOUT_TIME_SECONDS, FORCED_LOGOUT_TIME_SECONDS),
        path="/api/v1/userlogin/loginfromcookie",
        secure=True,
        httponly=True,
        samesite='strict'
    )
    return User(
        username=user_db.username,
        first_name=user_db.first_name,
        last_name=user_db.last_name,
        email=user_db.email,
        role=user_db.role,
        access_token=return_token,
        token_type="bearer",    # noqa: S106
        last_activity_unixtime=None,
        last_login_unixtime=None
    )


@router.post("/logout", tags=["login"])
async def logout(user: Annotated[User, Depends(get_current_user)], response: Response) -> None:
    """Logout endpoint."""
    print("Logout. Username:", user.username)
    await dal.update_user_data(user.username, {"access_token": None, "last_activity_unixtime": time.time()})
    response.delete_cookie(
        key="access_token",
        path="/api/v1/userlogin/loginfromcookie"
    )


async def get_user_out(user_db: UserSQL) -> User:
    """Convert UserSQL to User, replace token with empty string."""
    return User(
        username=user_db.username,
        first_name=user_db.first_name,
        last_name=user_db.last_name,
        email=user_db.email,
        role=user_db.role,
        access_token="",
        token_type="",
        last_activity_unixtime=user_db.last_activity_unixtime,
        last_login_unixtime=user_db.last_login_unixtime
    )


@router.get('/getallusers', response_model=list[User], status_code=200, tags=["user"])
async def get_user_list(current_user: Annotated[User, Depends(get_current_user_admin)]) -> list[User]:
    """
    Get all users endpoint (only admins).

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
async def create_user(current_user: Annotated[User, Depends(get_current_user_admin)], new_user: User):
    """
    Create new patient database entry (only admins).

    Parameters
    ----------
    new_user
        pydantic base model of new user, token_type should be "password" and
        access_token should contain the password of the new user.
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
    if new_user.token_type != "password":   # noqa: S105
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
        role=new_user.role.value,
        password_hash=hashed_received_password,
        salt=salt,
        access_token=None,
        last_activity_unixtime=None,
        last_login_unixtime=None
    )
    await dal.add_user(new_user_db)


@router.delete("/deleteuser", response_model={}, status_code=204, tags=["user"])
async def user_delete(current_user: Annotated[User, Depends(get_current_user_admin)], username_to_delete: str) -> None:
    """
    Delete an existing user (requires admin priviledges).

    Parameters
    ----------
    username_to_delete
        Name of the user to delete.

    Raises
    ------
    HTTPException
        404: Not found
    """
    # check if the this would delete the last user with admin role
    sql_user_to_delete = await dal.get_user_data(username_to_delete)
    if sql_user_to_delete is not None and sql_user_to_delete.role == UserRole.admin.value:
        at_least_two_admins = 0
        for user in await get_user_list(current_user):
            if user.role == UserRole.admin:
                at_least_two_admins += 1
                if at_least_two_admins >= 2:
                    break
        if at_least_two_admins < 2:
            raise HTTPException(status_code=403, detail="Cannot delete last admin.")
    # check if this deletes the current user
    if current_user.username == username_to_delete:
        raise HTTPException(status_code=403, detail="Cannot delete the user you are logged in with.")
    # try to delete if the user exists
    if not await dal.delete_user_data(username=username_to_delete):
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/updateuser", response_model={}, status_code=200, tags=["user"])
async def update_user(current_user: Annotated[User, Depends(get_current_user_admin)], updated_user: User) -> None:
    """
    Update the first_name, last_name, email and role of an existing user.

    Parameters
    ----------
    updated_user
        The attribute username identifies the user to modify.
        The attributes first_name, last_name, email and role are set for this user.

    Returns
    -------
        None

    Raises
    ------
    HTTPException
        404: Not found if user not found.
    """
    # check if the user exists
    sql_user_to_modify = await dal.get_user_data(updated_user.username)
    if sql_user_to_modify is None:
        raise HTTPException(status_code=403, detail="User does not exist.")
    # check if this would change the role of the last user with admin role
    if updated_user.role != UserRole.admin and sql_user_to_modify.role == UserRole.admin.value:
        at_least_two_admins = 0
        for user in await get_user_list(current_user):
            if user.role == UserRole.admin:
                at_least_two_admins += 1
                if at_least_two_admins >= 2:
                    break
        if at_least_two_admins < 2:
            raise HTTPException(status_code=403, detail="Cannot change role of last admin.")
    # do the update
    await dal.update_user_data(
        updated_user.username,
        {
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "email": updated_user.email,
            "role": updated_user.role.value,
        }
    )
