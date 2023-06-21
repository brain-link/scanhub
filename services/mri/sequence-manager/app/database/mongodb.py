# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""MongoDB database handle."""

import logging

from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


class Database:
    """MongoDB database handle.

    Attributes
    ----------
    client : AsyncIOMotorClient
        The MongoDB client.
    collection : AsyncIOMotorCollection
        The MongoDB collection.
    """

    client: AsyncIOMotorClient = None
    collection = None


# Create a global database handle.
db = Database()


async def connect_to_mongo():
    """Connect to MongoDB using the configuration settings."""
    logger.info("Connecting to MongoDB...")

    # global db

    connection_string = f"mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}"

    client = AsyncIOMotorClient(connection_string)

    if client_info := await client.server_info():
        logger.info(client_info)
    else:
        logger.info("Unable to connect to the server.")

    db.client = client[settings.MONGODB_DB]
    db.collection = client[settings.MONGODB_DB][settings.MONGODB_COLLECTION_NAME]


async def close_mongo_connection():
    """
    Close the connection to MongoDB.
    """
    logger.info("Closing MongoDB connection...")

    client = db.client
    client.close()
