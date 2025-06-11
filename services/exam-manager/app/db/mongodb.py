# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""MongoDB database handle."""

import os

from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase


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
    mongodb_username_filepath = "/run/secrets/sequence_database_root_username"
    mongodb_password_filepath = "/run/secrets/sequence_database_root_password"  # noqa: S105
    if (os.path.exists(mongodb_username_filepath) and \
        os.path.exists(mongodb_password_filepath)
    ):
        with open(mongodb_username_filepath) as file:
            mongodb_username = file.readline().strip()
        with open(mongodb_password_filepath) as file:
            mongodb_password = file.readline().strip()
        db_uri = f"mongodb://{mongodb_username}:{mongodb_password}@sequence-database:27017"
        print(f"Connecting to MongoDB at {db_uri}")
    else:
        raise RuntimeError("Database secrets for connection missing.")

    client: AsyncIOMotorClient = AsyncIOMotorClient(db_uri)

    if not (client_info := await client.server_info()):
        raise RuntimeError(f"Unable to connect to the server:\n{client_info}")

    db.client = client["mri_sequences_db"]
    db.collection = client["mri_sequences_db"]["mri_sequences"]


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
