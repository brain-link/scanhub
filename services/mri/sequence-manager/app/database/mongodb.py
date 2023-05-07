from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    """
    MongoDB database handle.
    
    Attributes:
    -----------
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
    """
    Connect to MongoDB using the configuration settings.
    """
    logger.info("Connecting to MongoDB...")

    global db

    connection_string = f"mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}"
    # connection_string = f"mongodb://{settings.MONGODB_USER}:{settings.MONGODB_PASSWORD}@{settings.MONGODB_HOST}:{settings.MONGODB_PORT}"

    client = AsyncIOMotorClient(connection_string)

    try:
        logger.info(await client.server_info())
    except Exception:
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
