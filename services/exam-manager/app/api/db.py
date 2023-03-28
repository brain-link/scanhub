import os
import asyncio

from sqlalchemy import create_engine, func, ForeignKey, MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime
from typing import List
from sqlalchemy.orm import relationship


# Create base for exam, record and procedure table
Base = declarative_base()
engine = create_engine(os.getenv('DB_URI'), echo=False)


def init_db() -> None:
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Exam(Base):
    """
    Exam ORM model
    """
    __tablename__ = 'exam'
    __table_args__ = {'extend_existing': True} 

    id: Mapped[int] = mapped_column(primary_key=True)
    # Relations and references
    procedures: Mapped[List["Procedure"]] = relationship(lazy="selectin")
    patient_id: Mapped[str] = mapped_column(nullable=False)
    # Fields
    name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=True)
    site: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)
    creator: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    datetime_created: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    datetime_updated: Mapped[datetime.datetime] = mapped_column(onupdate=func.now(), nullable=True)


class Procedure(Base):
    """
    Procedure ORM model
    """
    __tablename__ = 'procedure'
    __table_args__ = {'extend_existing': True} 

    id: Mapped[int] = mapped_column(primary_key=True)
    # Relations and references
    exam_id: Mapped[int] = mapped_column(ForeignKey("exam.id"))
    records: Mapped[List["Record"]] = relationship(lazy="selectin")
    # Fields
    name: Mapped[str] = mapped_column(nullable=False)
    modality: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    datetime_created: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    datetime_updated: Mapped[datetime.datetime] = mapped_column(onupdate=func.now(), nullable=True)


class Record(Base):
    """
    Record ORM model
    """
    __tablename__ = 'record'
    __table_args__ = {'extend_existing': True} 

    id: Mapped[int] = mapped_column(primary_key=True)

    # Relations and references
    procedure_id: Mapped[int] = mapped_column(ForeignKey("procedure.id"))
    workflow_id: Mapped[int] = mapped_column(nullable=True)
    device_id: Mapped[int] = mapped_column(nullable=False)
    # device_id: Mapped[int] = mapped_column(ForeignKey("device.id"))
    # device: Mapped["Device"] = relationship()
    sequence_id: Mapped[int] = mapped_column(nullable=False)
    # Fields
    status: Mapped[str] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(nullable=True)
    is_acquired: Mapped[bool] = mapped_column(nullable=False, default=False)
    datetime_created: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    datetime_updated: Mapped[datetime.datetime] = mapped_column(onupdate=func.now(), nullable=True)


# Create automap base
MappedBase = automap_base()
MappedBase.prepare(autoload_with=engine, reflect=True)

# Get existing models: device and workflow
try:
    Device = MappedBase.classes.device
    Workflow = MappedBase.classes.workflow
except AttributeError as e:
    print("***** ERROR: Table does not exist: ", e)


# Create async engine and session, echo=True generates console output
async_engine = create_async_engine(os.getenv('DB_URI_ASYNC'), future=True, echo=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
