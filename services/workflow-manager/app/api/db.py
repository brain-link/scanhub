import os

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI, echo=True)

Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# get workflow table
try:
    workflow = Base.classes.workflow
except ArithmeticError as err:
    print("Table does not exist: ", err)

database = Database(DATABASE_URI)
