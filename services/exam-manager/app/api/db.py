# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Database file for the MRI sequence manager service."""

import datetime
import os
import uuid

from pydantic import BaseModel
from scanhub_libraries.models import TaskStatus, TaskType
from sqlalchemy import JSON, ForeignKey, create_engine, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Create base for exam and job table
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


class Exam(Base):
    """Abstract exam ORM model."""

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    # Relations and references
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


class ExamDefinitions(Exam):
    """ORM model for exam definitions."""

    __tablename__ = "exam-definitions"
    __table_args__ = {"extend_existing": True}

    jobs: Mapped[list["JobDefinitions"]] = relationship(lazy="selectin")


class ExamTemplates(Exam):
    """ORM model for exam templates."""

    __tablename__ = "exam-templates"
    __table_args__ = {"extend_existing": True}

    jobs: Mapped[list["JobTemplates"]] = relationship(lazy="selectin")


class Job(Base): # TBD: rename to "Workflow"
    """Job ORM model."""

    __abstract__ = True

    # Use uuid here
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    # Relations and references
    # workflow_id: Mapped[int] = mapped_column(nullable=True)

    # Fields
    comment: Mapped[str] = mapped_column(nullable=True)
    # is_acquired: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_finished: Mapped[bool] = mapped_column(nullable=False, default=False)
    datetime_created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()  # pylint: disable=not-callable
    )
    datetime_updated: Mapped[datetime.datetime] = mapped_column(
        onupdate=func.now(), nullable=True  # pylint: disable=not-callable
    )


class JobDefinitions(Job):
    """ORM model for job definitions."""

    __tablename__ = "job-definitions"
    __table_args__ = {"extend_existing": True}

    tasks: Mapped[list["TaskDefinitions"]] = relationship(lazy="selectin")
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exam-definitions.id"))


class JobTemplates(Job):
    """ORM model for job templates."""

    __tablename__ = "job-templates"
    __table_args__ = {"extend_existing": True}

    tasks: Mapped[list["TaskTemplates"]] = relationship(lazy="selectin")
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exam-templates.id"))


class Task(Base):
    """Abstract task ORM model."""

    __abstract__ = True

    # Use uuid here
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    description: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[TaskType] = mapped_column(type_=JSON, nullable=False)

    # Arguments and parameters
    # Example: "args": {"arg1": "x", "arg2": "y"}
    args: Mapped[dict[str, str]] = mapped_column(type_=JSON, nullable=True)
    # acquisition_limits: Mapped[AcquisitionLimits] = mapped_column(type_=JSON, nullable=False)
    # sequence_parameters: Mapped[SequenceParameters] = mapped_column(type_=JSON, nullable=False)
    # device_parameters: Mapped[DeviceParameters] = mapped_column(type_=JSON, nullable=False)


    # Input and output artifacts with export destination
    # Example: {"input": [{"name": "env_HOLOSCAN_INPUT_PATH", "value": "{{ context.input.dicom }}"}]}
    # https://github.com/Project-MONAI/monai-deploy/blob/main/deploy/monai-deploy-express/sample-workflows/hello-world.json
    artifacts: Mapped[dict[str, list[dict[str, str]]]] = mapped_column(type_=JSON, nullable=True) # implemention of input and output artifacts for artifact types as replacement for string

    # List of task destinations, which are for example used to create the chain of topics in the kafka message broker, i.e., target topics
    task_destinations: Mapped[list[dict[str, str]]] = mapped_column(type_=JSON, nullable=True)

    status: Mapped[dict[TaskStatus, str]] = mapped_column(type_=JSON, nullable=False)

    # Fields
    datetime_created: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()  # pylint: disable=not-callable
    )


class TaskDefinitions(Task):
    """ORM model for task definitions."""

    __tablename__ = "task-definitions"
    __table_args__ = {"extend_existing": True}

    # Job references
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job-definitions.id"))

class TaskTemplates(Task):
    """ORM model for task templates."""

    __tablename__ = "task-templates"
    __table_args__ = {"extend_existing": True}

    # Job references
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job-templates.id"))

# TBD DeviceTask(Task):


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
