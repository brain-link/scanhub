# Copyright (C) 2025, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Security functions shared between the microservices."""
import http.client
import json
import time
from hashlib import scrypt, sha256
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import argon2

from scanhub_libraries.models import User

USERLOGIN_HOST = "user-login-manager:8000"
USERLOGIN_URI = "/api/v1/userlogin/getcurrentuser"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(access_token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    conn = http.client.HTTPConnection(USERLOGIN_HOST, timeout=5)
    try:
        conn.request("GET", USERLOGIN_URI, headers={"Authorization": f"Bearer {access_token}"})
        response = conn.getresponse()
        if response.status != 200:
            print("Received invalid token.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        body = response.read()
    finally:
        conn.close()  # ensures socket is closed

    data = json.loads(body)
    return User(username=data["username"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                role=data["role"],
                access_token="",
                token_type="",
                last_activity_unixtime=None,
                last_login_unixtime=None)


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