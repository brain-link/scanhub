# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Data acess layer (DAL) between fastapi endpoint and sql database for user data."""


from sqlalchemy.future import select

from app.db import UserSQL, async_session


async def get_user_data(username: str) -> (UserSQL | None):
    """Get user by username.

    Parameters
    ----------
    username
        Username as entered by the user. Primary key in db.

    Returns
    -------
        Database orm model of User or none
    """
    async with async_session() as session:
        user = await session.get(UserSQL, username)  # access by primary key "username"
    return user


async def update_user_data(username: str, data: dict) -> (UserSQL | None):
    """Update existing user entry.

    Parameters
    ----------
    username
        Primary key of the entry in db to be updated.

    data
        Data to be written. Does not need to contain all columns.

    Returns
    -------
        Database orm model of updated user
    """
    async with async_session() as session:
        if user_sql := await session.get(UserSQL, username):
            for key, value in data.items():
                getattr(user_sql, key)  # check if that column exists
                setattr(user_sql, key, value)
            await session.commit()
            await session.refresh(user_sql)
            return user_sql
        return None



async def get_user_from_token(access_token: str) -> (UserSQL | None):
    """Get user from token.

    Parameters
    ----------
    token
        Token. Unique in database.

    Returns
    -------
        The user as read from database or None if the token is not found.
    """
    async with async_session() as session:
        result = await session.scalars(select(UserSQL).where(UserSQL.access_token == access_token))
        user = result.first()
    return user


async def get_all_users() -> list[UserSQL]:
    """Get a list of all existing users.

    Returns
    -------
        List of database orm models
    """
    async with async_session() as session:
        result = await session.execute(select(UserSQL))
        users = list(result.scalars().all())
    return users


async def add_user(user: UserSQL):
    """Create a new user entry in database.

    Parameters
    ----------
    user
        UserSQL ORM model.

    Returns
    -------
        User database entry
    """
    async with async_session() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)


async def delete_user_data(username: str) -> bool:
    """Delete user by username.

    Parameters
    ----------
    username
        Username of the user to be deleted

    Returns
    -------
        Success of deletion
    """
    async with async_session() as session:
        if user := await session.get(UserSQL, username):
            await session.delete(user)
            await session.commit()
            return True
        return False
