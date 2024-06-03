from typing import Annotated
import time
import http.client
import json

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException

from scanhub_libraries.models import User


USERLOGIN_HOST = "user-login-manager:8000"
USERLOGIN_URI = "/api/v1/userlogin/getcurrentuser"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(access_token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    connection = http.client.HTTPConnection(USERLOGIN_HOST)
    connection.request("GET", USERLOGIN_URI, headers={"Authorization": "Bearer " + access_token})
    response = connection.getresponse()
    if response.status != 200:
        print("Received invalid token.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        responsebody = response.read()
        responsebody_json = json.loads(responsebody)
        return User(username=responsebody_json["username"],
                    first_name=responsebody_json["first_name"],
                    last_name=responsebody_json["last_name"],
                    email=responsebody_json["email"],
                    access_token="",
                    token_type="")