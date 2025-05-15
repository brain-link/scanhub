# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Patient database ORM model definition."""

import datetime
import os
import uuid
from typing import Literal

from pydantic import BaseModel
from scanhub_libraries.models import Gender
from sqlalchemy import create_engine, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped, mapped_column

# Create base for device
Base: DeclarativeMeta = declarative_base()


postgres_user_filepath = "/run/secrets/patient_database_postgres_user"
postgres_password_filepath = "/run/secrets/patient_database_postgres_password"
postgres_db_name_filepath = "/run/secrets/patient_database_postgres_db_name"
if (os.path.exists(postgres_user_filepath) and \
    os.path.exists(postgres_password_filepath) and \
    os.path.exists(postgres_db_name_filepath) \
):
    with open(postgres_user_filepath) as file:
        postgres_user = file.readline().strip()
    with open(postgres_password_filepath) as file:
        postgres_password = file.readline().strip()
    with open(postgres_db_name_filepath) as file:
        postgres_db_name = file.readline().strip()
    db_uri = f"postgresql://{postgres_user}:{postgres_password}@patient-database/{postgres_db_name}"
    db_uri_async = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@patient-database/{postgres_db_name}"
    engine = create_engine(db_uri, echo=False)
    # Create async engine and session, echo=True generates console output
    async_engine = create_async_engine(db_uri_async, future=True, echo=False, isolation_level="AUTOCOMMIT")
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)
else:
    raise RuntimeError("Database secrets for connection missing.")


def init_db() -> None:
    """Initialize database."""
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Patient(Base):
    """Patient ORM model."""

    __tablename__ = 'patients'
    patient_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

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
