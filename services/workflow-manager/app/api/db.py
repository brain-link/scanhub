import os

from sqlalchemy import Column, Integer, MetaData, String, DateTime, Table, create_engine, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI, echo=True)
metadata = MetaData()

# Generate declarative base class
Base = declarative_base()

# Workflow database model
class Workflow(Base):
    __tablename__ = 'workflow'

    id = Column(Integer, primary_key=True)
    
    # One-to-many (workflow to records), bidirectional
    # TODO: How to do the mapping, record db model in different container
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


# Base.metadata.tables["workflow"].create(bind=engine)
Base.metadata.create_all(engine)
database = Database(DATABASE_URI)

