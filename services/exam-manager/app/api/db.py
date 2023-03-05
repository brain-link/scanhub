import os

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI, echo=True)

Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# mapped classes are now created with names by default
# matching that of the table name.
try:
    exam = Base.classes.exam
    procedure = Base.classes.procedure
    record = Base.classes.record
except ArithmeticError as err:
    print("Table does not exist: ", err)

database = Database(DATABASE_URI)




# Generate declarative base class
# Base = declarative_base()

# # Exam database model
# class Exam(Base):
#     __tablename__ = 'exam'

#     id = Column(Integer, primary_key=True)
#     patient_id = Column(String(50), nullable=False)

#     # One-to-many (exam to procedures), bidirectional
#     procedure = relationship("Procedure", back_populates="exam")

#     datetime_created = Column(DateTime(timezone=True), server_default=func.now())
#     datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
#     name = Column(String(50), nullable=False)
#     country = Column(String(50), nullable=True)
#     site = Column(String(50), nullable=True)
#     address = Column(String(100), nullable=True)
#     creator = Column(String(50), nullable=False)
#     status = Column(String(50), nullable=False)


# # Procedure database model
# class Procedure(Base):
#     __tablename__ = 'procedure'

#     id = Column(Integer, primary_key=True)
    
#     # Many-to-one (procedures to exam), bidirectional
#     exam_id = Column(Integer, ForeignKey('exam.id'), nullable=False)
#     exam = relationship("Exam", back_populates="procedures")

#     # One-to-man (procedure to records)
#     records = relationship("Record", back_populates="procedure")

#     datetime_created = Column(DateTime(timezone=True), server_default=func.now())
#     datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
#     name = Column(String(50), nullable=False)
#     modality = Column(String(50), nullable=False)
#     status = Column(String(50), nullable=False)


# # Record database model
# class Record(Base):
#     __tablename__ = 'record'

#     id = Column(Integer, primary_key=True)

#     # Many-to-one (records to procedure), bidirectional
#     procedure_id = Column(Integer, ForeignKey('procedure.id'), nullable=False)
#     procedure = relationship("Procedure", back_populates="record")

#     # One-to-one relation (workflow to record)
#     # TODO: How to do the mapping, db model in different container
#     # workflow_id = Column(Integer, ForeignKey('workflow.id'), nullable=True)
#     workflow_id = Column(Integer, nullable=True)
#     # workflow = relationship("Workflow")

#     # One-to-one relation (device to record)
#     # TODO: How to do the mapping, db model in different container
#     # device_id = Column(Integer, ForeignKey('device.id'), nullable=False)
#     device_id = Column(Integer, nullable=False)
#     # device = relationship("Device")

#     sequence_id = Column(Integer, nullable=True)
#     datetime_created = Column(DateTime(timezone=True), server_default=func.now())
#     datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
#     status = Column(String(50), nullable=False)
#     comment = Column(String, nullable=True)

# Base.metadata.create_all(engine)
# # Base.metadata.tables["exam", "procedure", "record"].create(bind=engine)
# database = Database(DATABASE_URI)