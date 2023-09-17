# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of workflow database ORM model."""

import datetime
import os

from pydantic import BaseModel
from sqlalchemy import JSON
from sqlalchemy import create_engine, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.orm.decl_api import DeclarativeMeta

from typing import Any

# Create base for device
Base: DeclarativeMeta = declarative_base()

if db_uri := os.getenv("DB_URI"):
    engine = create_engine(db_uri, echo=False)
else:
    raise RuntimeError("Database URI not defined.")


def init_db() -> None:
    """Initialize the database."""
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Workflow(Base):
    """Device ORM model."""

    __tablename__ = "workflow"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    version: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    definition: Mapped[dict[str,Any]] = mapped_column(type_=JSON, nullable=False)

    datetime_created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()  # pylint: disable=not-callable
    )
    datetime_updated: Mapped[datetime.datetime] = mapped_column(
        onupdate=func.now(), nullable=True  # pylint: disable=not-callable
    )

    def update(self, data: BaseModel):
        """Update workflow database entries.

        Parameters
        ----------
        data
            Pydantic base model with data to be updated
        """
        for key, value in data.dict().items():
            setattr(self, key, value)


if db_uri_async := os.getenv("DB_URI_ASYNC"):
    # Create async engine and session, echo=True generates console output
    async_engine = create_async_engine(
        db_uri_async,
        future=True,
        echo=False,
        isolation_level="AUTOCOMMIT",
    )
else:
    raise RuntimeError("Database URI not defined.")

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
