# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""MongoDB database handle."""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase
from app.db.mongodb_config import settings
from fastapi import HTTPException, status


class Database:
    """MongoDB database handle.

    Attributes
    ----------
    client : AsyncIOMotorClient
        The MongoDB client.
    collection : AsyncIOMotorCollection
        The MongoDB collection.
    """
    # TODO: Can the client really take two different types?
    client: AsyncIOMotorClient | AsyncIOMotorDatabase | None = None
    collection: AsyncIOMotorCollection | None = None

# Create a global database handle.
db = Database()

async def connect_to_mongo():
    """Connect to MongoDB using the configuration settings."""
    connection_string = f"mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}"

    client: AsyncIOMotorClient = AsyncIOMotorClient(connection_string)

    if client_info := await client.server_info():
        print(client_info)
    else:
        print("Unable to connect to the server.")

    db.client = client[settings.MONGODB_DB]
    db.collection = client[settings.MONGODB_DB][settings.MONGODB_COLLECTION_NAME]


async def close_mongo_connection():
    """Close the connection to MongoDB."""
    if isinstance(db.client, AsyncIOMotorClient):
        db.client.close()


def get_mongo_database() -> Database:
    """Dependency for getting a handle to the MongoDB database."""
    if db is not None:
        return db
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database not connected",
    )