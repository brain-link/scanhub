import os

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(os.getenv('DATABASE_URI'), echo=True)

Base = declarative_base()


# Exam database model
class Exam(Base):
    __tablename__ = 'exam'

    id = Column(Integer, primary_key=True)
    patient_id = Column(String(50), nullable=False)

    # One-to-many (exam to procedures), bidirectional
    procedure = relationship("Procedure", back_populates="exam")

    datetime_created = Column(DateTime(timezone=True), server_default=func.now())
    datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(50), nullable=False)
    country = Column(String(50), nullable=True)
    site = Column(String(50), nullable=True)
    address = Column(String(100), nullable=True)
    creator = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)


# Procedure database model
class Procedure(Base):
    __tablename__ = 'procedure'

    id = Column(Integer, primary_key=True)
    
    # Many-to-one (procedures to exam), bidirectional
    exam_id = Column(Integer, ForeignKey('exam.id'), nullable=False)
    exam = relationship("Exam", back_populates="procedures")

    # One-to-man (procedure to records)
    records = relationship("Record", back_populates="procedure")

    datetime_created = Column(DateTime(timezone=True), server_default=func.now())
    datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(50), nullable=False)
    modality = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)


# Record database model
class Record(Base):
    __tablename__ = 'record'

    id = Column(Integer, primary_key=True)

    # Many-to-one (records to procedure), bidirectional
    procedure_id = Column(Integer, ForeignKey('procedure.id'), nullable=False)
    procedure = relationship("Procedure", back_populates="record")

    # One-to-one relation (workflow to record)
    workflow_id = Column(Integer, ForeignKey('workflow.id'), nullable=True)
    workflow = relationship("Workflow")

    # One-to-one relation (device to record)
    device_id = Column(Integer, ForeignKey('device.id'), nullable=False)
    device = relationship("Device")

    sequence_id = Column(Integer, nullable=True)
    datetime_created = Column(DateTime(timezone=True), server_default=func.now())
    datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(String(50), nullable=False)
    comment = Column(String, nullable=True)


# Device database model
class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    
    # One-to-many (device to records), bidirectional
    # records = relationship("Record", back_populates="device")

    datetime_created = Column(DateTime(timezone=True), server_default=func.now())
    datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(50), nullable=False)
    manufacturer = Column(String(50), nullable=False)
    modality = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    site = Column(String(50), nullable=True)
    ip_address = Column(String(50), nullable=False)


# Workflow database model
class Workflow(Base):
    __tablename__ = 'workflow'

    id = Column(Integer, primary_key=True)
    
    # One-to-many (workflow to records), bidirectional
    # records = relationship("Record", back_populates="workflow")

    datetime_created = Column(DateTime(timezone=True), server_default=func.now())
    datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
    host = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    manufacturer = Column(String(50), nullable=False)
    modality = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    kafka_topic = Column(String(50), nullable=False)


Base.metadata.create_all(engine)