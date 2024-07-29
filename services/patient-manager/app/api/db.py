# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Patient database ORM model definition."""

import datetime
import os
from typing import Literal

from pydantic import BaseModel
from sqlalchemy import create_engine, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped, mapped_column

from scanhub_libraries.models import Gender

# Create base for device
Base: DeclarativeMeta = declarative_base()

if (db_uri := os.getenv('DB_URI')):
    engine = create_engine(db_uri, echo=False)
else:
    raise RuntimeError("Invalid environment variable DB_URI")


def init_db() -> None:
    """Initialize database."""
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Patient(Base):
    """Patient ORM model."""

    __tablename__ = 'patients'

    patient_id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[datetime.date] = mapped_column(nullable=False)
    sex: Mapped[Gender] = mapped_column(nullable=False)
    issuer: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[Literal["NEW", "UPDATED", "DELETED"]] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(nullable=True)

    datetime_created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now())  # pylint: disable=not-callable
    datetime_updated: Mapped[datetime.datetime] = mapped_column(
        onupdate=func.now(), nullable=True)  # pylint: disable=not-callable

    def update(self, data: BaseModel):
        """Update a patient entry.

        Parameters
        ----------
        data
            Data to be written
        """
        for key, value in data.dict().items():
            setattr(self, key, value)


# Create async engine and session, echo=True generates console output
if (async_db_uri := os.getenv('DB_URI_ASYNC')):
    async_engine = create_async_engine(
        async_db_uri,
        future=True,
        echo=False,
        isolation_level="AUTOCOMMIT",
    )
else:
    raise RuntimeError("Invalid environment variable DB_URI_ASYNC")

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
