# # Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# # SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

# """Database file for the MRI sequence manager service."""

# import datetime
import os
# import uuid

from pydantic import BaseModel
# from scanhub_libraries.models import TaskStatus, TaskType
# from sqlalchemy import JSON, ForeignKey, create_engine, func
from sqlalchemy import create_engine
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
# from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Create base for exam and workflow table
class Base(DeclarativeBase):
    """Declarative base class."""

    def update(self, data: BaseModel) -> None:
        """Update a exam entry.

        Parameters
        ----------
        data
            Data to be written
        """
        for key, value in data.dict().items():
            setattr(self, key, value)


if db_uri := os.getenv("DB_URI"):
    engine = create_engine(db_uri, echo=False)
else:
    raise RuntimeError("Database URI not defined.")


def init_db() -> None:
    """Initialize the database."""
    Base.metadata.create_all(engine)


class User(Base):
    """Abstract exam ORM model."""

    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    username: Mapped[str] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)



# # Create automap base
# MappedBase = automap_base()
# MappedBase.prepare(autoload_with=engine, reflect=True)

# # Get existing device models
# try:
#     Device = MappedBase.classes.device
# except AttributeError as error:
#     raise AttributeError("Could not find device and/or workflow table(s).") from error


# if db_uri_async := os.getenv("DB_URI_ASYNC"):
#     # Create async engine and session, echo=True generates console output
#     async_engine = create_async_engine(db_uri_async, future=True, echo=False, isolation_level="AUTOCOMMIT")
# else:
#     raise RuntimeError("Database URI not defined.")

# async_session = async_sessionmaker(async_engine, expire_on_commit=False)
