import os

from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)

from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

devices = Table(
    'devices',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('host', String(50)),
    Column('manufacturer', String(50)),
    Column('model', String(50)),
    Column('type', String(50)),
    Column('serial_number', String(50)),
    Column('kafka_topic', String(50)),
    Column('status', String(50)),
)

database = Database(DATABASE_URI)