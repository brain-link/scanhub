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
    workflow = Base.classes.workflow
except ArithmeticError as err:
    print("Table does not exist: ", err)

database = Database(DATABASE_URI)

# # Workflow database model
# class Workflow(Base):
#     __tablename__ = 'workflow'

#     id = Column(Integer, primary_key=True)
    
#     # One-to-many (workflow to records), bidirectional
#     # TODO: How to do the mapping, record db model in different container
#     # records = relationship("Record", back_populates="workflow")

#     datetime_created = Column(DateTime(timezone=True), server_default=func.now())
#     datetime_updated = Column(DateTime(timezone=True), onupdate=func.now())
#     host = Column(String(50), nullable=False)
#     name = Column(String(50), nullable=False)
#     manufacturer = Column(String(50), nullable=False)
#     modality = Column(String(50), nullable=False)
#     type = Column(String(50), nullable=False)
#     status = Column(String(50), nullable=False)
#     kafka_topic = Column(String(50), nullable=False)


# Base.metadata.create_all(engine)
# database = Database(DATABASE_URI)

