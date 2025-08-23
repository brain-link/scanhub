# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of device database ORM models."""

import datetime
import os
import uuid

from sqlalchemy import JSON, create_engine, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.orm.decl_api import DeclarativeMeta

# Create base for device
Base: DeclarativeMeta = declarative_base()


postgres_user_filepath = "/run/secrets/scanhub_database_postgres_user"
postgres_password_filepath = "/run/secrets/scanhub_database_postgres_password"  # noqa: S105
postgres_db_name_filepath = "/run/secrets/scanhub_database_postgres_db_name"
if (os.path.exists(postgres_user_filepath) and
    os.path.exists(postgres_password_filepath) and
    os.path.exists(postgres_db_name_filepath)
):
    with open(postgres_user_filepath) as file:
        postgres_user = file.readline().strip()
    with open(postgres_password_filepath) as file:
        postgres_password = file.readline().strip()
    with open(postgres_db_name_filepath) as file:
        postgres_db_name = file.readline().strip()
    db_uri = f"postgresql://{postgres_user}:{postgres_password}@scanhub-database/{postgres_db_name}"
    db_uri_async = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@scanhub-database/{postgres_db_name}"
    engine = create_engine(db_uri, echo=False)
    # Create async engine and session, echo=True generates console output
    async_engine = create_async_engine(db_uri_async, future=True, echo=False, isolation_level="AUTOCOMMIT")
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)
else:
    raise RuntimeError("Database secrets for connection missing.")


def init_db() -> None:
    """Create database helper function."""
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Device(Base):  # type: ignore
    """Device ORM model."""

    __tablename__ = "device"

    # Main identifiers
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    # Secrets
    token_hash: Mapped[str] = mapped_column(nullable=False, unique=True)
    salt: Mapped[str] = mapped_column(nullable=False)

    # Details
    device_name: Mapped[str] = mapped_column(nullable=True)
    serial_number: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)
    manufacturer: Mapped[str] = mapped_column(nullable=True)
    modality: Mapped[str] = mapped_column(nullable=True)
    site: Mapped[str] = mapped_column(nullable=True)
    parameter: Mapped[dict] = mapped_column(type_=JSON, nullable=True)

    datetime_created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()  # pylint: disable=not-callable
    )
    datetime_updated: Mapped[datetime.datetime] = mapped_column(
        onupdate=func.now(), nullable=True  # pylint: disable=not-callable
    )

    def update(self, data: dict) -> None:
        """Update attributes of orm model.

        Parameters
        ----------
            data {dict} -- Entries to be updated
        """
        for key, value in data.items():
            setattr(self, key, value)
