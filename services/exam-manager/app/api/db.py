# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Database file for the MRI sequence manager service."""

import datetime
import os
from enum import Enum

from pydantic import BaseModel, Field
from sqlalchemy import JSON, ForeignKey, create_engine, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Create base for exam, record and procedure table
Base: DeclarativeMeta = declarative_base()

if db_uri := os.getenv("DB_URI"):
    engine = create_engine(db_uri, echo=False)
else:
    raise RuntimeError("Database URI not defined.")


def init_db() -> None:
    """Initialize the database."""
    Base.metadata.create_all(engine)


class XYZ(BaseModel):
    """XYZ model."""

    X: float
    Y: float
    Z: float


class SequenceParameters(BaseModel):
    """SequenceParameters model."""

    fov: XYZ
    fov_offset: XYZ


class Gender(str, Enum):
    """Gender model."""

    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    NOT_GIVEN = "NOT_GIVEN"


class AcquisitionLimits(BaseModel):
    """AcquisitionLimits models."""

    patient_height: float
    patient_weight: float
    patient_gender: Gender = Field(None, alias="Gender")
    patient_age: int


class Exam(Base):
    """Exam ORM model."""

    __tablename__ = "exam"
    __table_args__ = {"extend_existing": True}

    # Use uuid here
    id: Mapped[int] = mapped_column(primary_key=True)

    # Relations and references
    procedures: Mapped[list["Procedure"]] = relationship(lazy="selectin")
    patient_id: Mapped[int] = mapped_column(nullable=False)

    # Fields
    name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=True)
    site: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)
    creator: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

    datetime_created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()  # pylint: disable=not-callable
    )
    datetime_updated: Mapped[datetime.datetime] = mapped_column(
        onupdate=func.now(), nullable=True  # pylint: disable=not-callable
    )

    def update(self, data: BaseModel) -> None:
        """Update a exam entry.

        Parameters
        ----------
        data
            Data to be written
        """
        for key, value in data.dict().items():
            setattr(self, key, value)


class Procedure(Base):
    """Procedure ORM model."""

    __tablename__ = "procedure"
    __table_args__ = {"extend_existing": True}

    # Use uuid here
    id: Mapped[int] = mapped_column(primary_key=True)

    # Relations and references
    exam_id: Mapped[int] = mapped_column(ForeignKey("exam.id"))
    jobs: Mapped[list["Job"]] = relationship(lazy="selectin")

    # Fields
    name: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    datetime_created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()  # pylint: disable=not-callable
    )
    datetime_updated: Mapped[datetime.datetime] = mapped_column(
        onupdate=func.now(), nullable=True  # pylint: disable=not-callable
    )

    def update(self, data: BaseModel) -> None:
        """Update a procedure entry.

        Parameters
        ----------
        data
            Data to be written
        """
        for key, value in data.dict().items():
            setattr(self, key, value)


class Job(Base):
    """Job ORM model."""

    __tablename__ = "job"
    __table_args__ = {"extend_existing": True}

    # Use uuid here
    id: Mapped[int] = mapped_column(primary_key=True)

    # Relations and references
    procedure_id: Mapped[int] = mapped_column(ForeignKey("procedure.id"))
    workflow_id: Mapped[int] = mapped_column(nullable=True)
    device_id: Mapped[str] = mapped_column(nullable=True)
    sequence_id: Mapped[str] = mapped_column(nullable=False)
    records: Mapped[list["Record"]] = relationship(lazy="selectin")

    # Fields
    type: Mapped[str] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(nullable=True)
    is_acquired: Mapped[bool] = mapped_column(nullable=False, default=False)
    datetime_created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()  # pylint: disable=not-callable
    )
    datetime_updated: Mapped[datetime.datetime] = mapped_column(
        onupdate=func.now(), nullable=True  # pylint: disable=not-callable
    )
    acquisition_limits: Mapped[AcquisitionLimits] = mapped_column(type_=JSON, nullable=False)
    sequence_parameters: Mapped[SequenceParameters] = mapped_column(type_=JSON, nullable=False)

    def update(self, data: BaseModel) -> None:
        """Update a job entry.

        Parameters
        ----------
        data
            Data to be written
        """
        for key, value in data.dict().items():
            setattr(self, key, value)


class Record(Base):
    """Record ORM model."""

    __tablename__ = "record"
    __table_args__ = {"extend_existing": True}

    # Use uuid here
    id: Mapped[int] = mapped_column(primary_key=True)
    # Relations and references
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))
    data_path: Mapped[str] = mapped_column(nullable=True)
    # Fields
    comment: Mapped[str] = mapped_column(nullable=True)
    datetime_created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()  # pylint: disable=not-callable
    )

    def update(self, data: dict) -> None:
        """Update a Record entry.

        Parameters
        ----------
        data
            Data to be written
        """
        print(type(data))
        for key, value in data.items():
            setattr(self, key, value)


# Create automap base
MappedBase = automap_base()
MappedBase.prepare(autoload_with=engine, reflect=True)

# Get existing models: device and workflow
try:
    Device = MappedBase.classes.device
    Workflow = MappedBase.classes.workflow
except AttributeError as error:
    raise AttributeError("Could not find device and/or workflow table(s).") from error


if db_uri_async := os.getenv("DB_URI_ASYNC"):
    # Create async engine and session, echo=True generates console output
    async_engine = create_async_engine(db_uri_async, future=True, echo=False, isolation_level="AUTOCOMMIT")
else:
    raise RuntimeError("Database URI not defined.")

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
