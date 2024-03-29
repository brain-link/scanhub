# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Configuration file for the MRI sequence manager service."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """The Settings class represents the configuration settings for the application.

    Attributes
    ----------
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
        """Base settings configuration."""

        env_file = ".env"


# Create settings instance
# settings = Settings()     # throws mypy error: missing named aarguments # pyright: ignore
# Possible solution according to https://github.com/pydantic/pydantic/issues/3753:
settings = Settings.parse_obj({})
