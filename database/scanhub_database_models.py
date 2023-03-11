import os
import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID


# Use sync engine to create ORM models
engine = create_engine(os.getenv('DATABASE_URI'), echo=True)
Base = declarative_base()


# Exam database model
class Exam(Base):
    __tablename__ = 'exam'

    # id: Mapped[int] = mapped_column(primary_key=True)

    # datetime_created: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    # datetime_updated: Mapped[datetime.datetime] = mapped_column(onupdate=func.now())

    # # One-to-many (exam to procedures), bidirectional
    # procedures = relationship("Procedure", back_populates="exams")

    # patient_id: Mapped[str] = mapped_column(nullable=False)
    # name: Mapped[str] = mapped_column(nullable=False)
    # country: Mapped[str] = mapped_column(nullable=True)
    # site: Mapped[str] = mapped_column(nullable=True)
    # address: Mapped[str] = mapped_column(nullable=True)
    # creator: Mapped[str] = mapped_column(nullable=False)
    # status: Mapped[str] = mapped_column(nullable=False)


    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    
    datetime_created = Column(DateTime(timezone=True), server_default=func.now())
    datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())

    patient_id = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    country = Column(String(50), nullable=True)
    site = Column(String(50), nullable=True)
    address = Column(String(100), nullable=True)
    creator = Column(String(50), nullable=False)
    # TODO: Use enum to describe exam status
    status = Column(String(50), nullable=False)

    procedures = relationship("Procedure", backref="exam")


# Procedure database model
class Procedure(Base):
    __tablename__ = 'procedure'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    
    # Many-to-one (procedures to exam), bidirectional
    exam_id = Column(ForeignKey('exam.id'))
    # exams = relationship("Exam", back_populates="procedures")

    # One-to-many (procedure to records)
    # records = relationship("Record", back_populates="procedure")

    datetime_created = Column(DateTime(timezone=True), server_default=func.now())
    datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(50), nullable=False)
    # TODO: Use enum to describe procedure modality
    modality = Column(String(50), nullable=False)
    # TODO: Use enum to describe procedure status
    status = Column(String(50), nullable=False)


# Record database model
class Record(Base):
    __tablename__ = 'record'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    # Many-to-one (records to procedure), bidirectional
    procedure_id = Column(UUID, ForeignKey('procedure.id'), nullable=False)
    # procedure = relationship("Procedure", back_populates="record")

    # One-to-one relation (workflow to record)
    workflow_id = Column(UUID, ForeignKey('workflow.id'), nullable=True)
    workflow = relationship("Workflow")

    # One-to-one relation (device to record)
    device_id = Column(UUID, ForeignKey('device.id'), nullable=False)
    device = relationship("Device")

    sequence_id = Column(Integer, nullable=True)
    datetime_created = Column(DateTime(timezone=True), server_default=func.now())
    datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
    # TODO: Use enum to describe record status
    status = Column(String(50), nullable=False)
    comment = Column(String, nullable=True)
    is_acquired = Column(Boolean, nullable=False, default=False)


# Device database model
class Device(Base):
    __tablename__ = 'device'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    
    # One-to-many (device to records), bidirectional
    # records = relationship("Record", back_populates="device")

    datetime_created = Column(DateTime(timezone=True), server_default=func.now())
    datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(50), nullable=False)
    manufacturer = Column(String(50), nullable=False)
    # TODO: Use enum to describe procedure status
    modality = Column(String(50), nullable=False)
    # TODO: Use enum to describe device status
    status = Column(String(50), nullable=False)
    site = Column(String(50), nullable=True)
    ip_address = Column(String(50), nullable=False)


# Workflow database model
class Workflow(Base):
    __tablename__ = 'workflow'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    
    # One-to-many (workflow to records), bidirectional
    # records = relationship("Record", back_populates="workflow")

    datetime_created = Column(DateTime(timezone=True), server_default=func.now())
    datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
    host = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    manufacturer = Column(String(50), nullable=False)
    # TODO: Use enum to describe workflow modality
    modality = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    # TODO: Use enum to describe workflow status
    status = Column(String(50), nullable=False)
    kafka_topic = Column(String(50), nullable=False)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)