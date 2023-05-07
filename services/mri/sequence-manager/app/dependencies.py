from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from database.mongodb import db, connect_to_mongo, close_mongo_connection

def get_database() -> AsyncIOMotorDatabase:
    """
    Dependency for getting a handle to the MongoDB database.
    """
    if db is not None:
        return db
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database not connected")
