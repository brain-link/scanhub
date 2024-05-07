from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI, HTTPException, status

from scanhub_libraries.models import User

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: Annotated[str, Depends(_oauth2_scheme)]):
    if token == "Bitte":
        return User(username="maxi123", first_name="Maximiliane", last_name="Musterfrau", email="maxi123mail@mail.de")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )