import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.automap import automap_base

DATABASE_URI = os.getenv('DATABASE_URI')


Base = automap_base()
# Create sync engine for automap function
engine = create_engine(DATABASE_URI)    #, echo=True)

# Reflect the tables
Base.prepare(engine, reflect=True)

# Get ORM models
try:
    Exam = Base.classes.exam
    Procedure = Base.classes.procedure
    Record = Base.classes.record
    Device = Base.classes.device
    Workflow = Base.classes.workflow
    # exam_table = Base.metadata.tables["exam"]
    # procedure_table = Base.metadata.tables["procedure"]
    # record_table = Base.metadata.tables["record"]
except AttributeError as err:
    print("Table does not exist: ", err)

# Create async engine and session, echo=True generates console output
async_engine = create_async_engine(os.getenv('DATABASE_URI_ASYNCPG'), future=True)  #, echo=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

# async def get_session() -> AsyncSession:
#     async_session = async_sessionmaker(async_engine, expire_on_commit=False)
#     with async_session() as session:
#         yield session