import os

from sqlalchemy import Column, Integer, MetaData, DateTime, String, Table, create_engine, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI, echo=True)
metadata = MetaData()

# Generate declarative base class
Base = declarative_base()

# Device database model
class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    
    # One-to-many (device to records), bidirectional
    # TODO: How to do the mapping, record db model in different container
    # records = relationship("Record", back_populates="device")

    datetime_created = Column(DateTime(timezone=True), server_default=func.now())
    datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String(50), nullable=False)
    manufacturer = Column(String(50), nullable=False)
    modality = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    site = Column(String(50), nullable=True)
    ip_address = Column(String(50), nullable=False)

# Base.metadata.tables["device"].create(bind=engine)
Base.metadata.create_all(engine)
database = Database(DATABASE_URI)