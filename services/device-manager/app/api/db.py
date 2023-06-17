# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of device database ORM models."""

import datetime
import os

from sqlalchemy import create_engine, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.orm.decl_api import DeclarativeMeta

# Create base for device
Base: DeclarativeMeta = declarative_base()

if db_uri := os.getenv("DB_URI"):
    engine = create_engine(db_uri, echo=False)
else:
    raise RuntimeError("Database URI not defined.")


def init_db() -> None:
    """Create database helper function."""
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Device(Base):
    """Device ORM model."""

    __tablename__ = "device"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)
    manufacturer: Mapped[str] = mapped_column(nullable=False)
    modality: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    site: Mapped[str] = mapped_column(nullable=True)
    ip_address: Mapped[str] = mapped_column(nullable=False)

    datetime_created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )
    datetime_updated: Mapped[datetime.datetime] = mapped_column(
        onupdate=func.now(), nullable=True
    )

    def update(self, data: dict):
        """Update attributes of orm model.

        Arguments:
            data {dict} -- Entries to be updated
        """
        for key, value in data.items():
            setattr(self, key, value)


if db_uri_async := os.getenv("DB_URI_ASYNC"):
    # Create async engine and session, echo=True generates console output
    async_engine = create_async_engine(
        db_uri_async, future=True, echo=False, isolation_level="AUTOCOMMIT"
    )
else:
    raise RuntimeError("Database URI not defined.")

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
