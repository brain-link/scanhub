from typing import Annotated
import time

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI, HTTPException, status

from scanhub_libraries.dal import get_user_from_token, update_user_data
from scanhub_libraries.db import UserSQL


AUTOMATIC_LOGOUT_TIME_SECONDS = 3600  # time until a login token gets invalid (1 hour)


_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(access_token: Annotated[str, Depends(_oauth2_scheme)]) -> UserSQL:
    user: UserSQL = await get_user_from_token(access_token)
    if user is not None and user.access_token is not None and user.last_activity_unixtime is not None \
            and time.time() - user.last_activity_unixtime < AUTOMATIC_LOGOUT_TIME_SECONDS:              # auto-logout time 1 hour
        await update_user_data(user.username, {"last_activity_unixtime": time.time()})         # reset last_activity timer
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token.",
        headers={"WWW-Authenticate": "Bearer"},
    )