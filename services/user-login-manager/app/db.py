# # Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# # SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Database file for the user-login-manager service, user authentication check and other general purpose tasks."""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Define base class.

    DeclarativeBase cannot be used directly.
    """

    pass


if db_uri := os.getenv("DB_URI"):
    engine = create_engine(db_uri, echo=False)
else:
    raise RuntimeError("Database URI not defined.")


def init_db() -> None:
    """Initialize the database."""
    Base.metadata.create_all(engine)


class UserSQL(Base):
    """User ORM model."""

    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    username: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    # salt used to create the password_hash
    salt: Mapped[str] = mapped_column(nullable=False)
    # token used to access backend while user is logged in, None if user is logged out
    access_token: Mapped[str] = mapped_column(nullable=True, unique=True)
    # time of last activity, used for automatic logout
    last_activity_unixtime: Mapped[int] = mapped_column(nullable=True)



# # Create automap base
# MappedBase = automap_base()
# MappedBase.prepare(autoload_with=engine, reflect=True)

# # Get existing device models
# try:
#     Device = MappedBase.classes.device
# except AttributeError as error:
#     raise AttributeError("Could not find device and/or workflow table(s).") from error


if db_uri_async := os.getenv("DB_URI_ASYNC"):
    # Create async engine and session, echo=True generates console output
    async_engine = create_async_engine(db_uri_async, future=True, echo=False, isolation_level="AUTOCOMMIT")
else:
    raise RuntimeError("Database URI not defined.")

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
