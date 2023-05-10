from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    The Settings class represents the configuration settings for the application.

    Attributes:
    -----------
    MONGODB_USER : str
        The username for authenticating to the MongoDB server.
    MONGODB_PASSWORD : str
        The password for authenticating to the MongoDB server.
    MONGODB_HOST : str
        The hostname of the MongoDB server.
    MONGODB_PORT : int
        The port number for connecting to the MongoDB server.
    MONGODB_DB : str
        The name of the MongoDB database used for storing MRI sequence data.
    MONGODB_COLLECTION_NAME : str
        The name of the MongoDB collection used for storing MRI sequence data.
    """

    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_DB: str
    MONGODB_COLLECTION_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()

