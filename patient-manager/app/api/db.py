"""Patient database ORM model definition."""

import datetime
import os

from sqlalchemy import create_engine, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from .models import BasePatient

# Create base for device
Base = declarative_base()

if (db_uri := os.getenv('DB_URI')):
    engine = create_engine(db_uri, echo=False)
else:
    raise RuntimeError("Invalid environment variable DB_URI")


def init_db() -> None:
    """Initialize database."""
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Patient(Base):
    """Patient ORM model."""

    __tablename__ = 'patients'

    patient_id: Mapped[int] = mapped_column(primary_key=True)

    sex: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[str] = mapped_column(nullable=False)
    issuer: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(nullable=False)

    datetime_created: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    datetime_updated: Mapped[datetime.datetime] = mapped_column(onupdate=func.now(), nullable=True)

    def update(self, data: BasePatient):
        """Update a patient entry.

        Parameters
        ----------
        data
            Data to be written
        """
        for key, value in data.dict().items():
            setattr(self, key, value)


# Create async engine and session, echo=True generates console output
if (async_db_uri := os.getenv('DB_URI_ASYNC')):
    async_engine = create_async_engine(
        async_db_uri,
        future=True,
        echo=False,
        isolation_level="AUTOCOMMIT",
    )
else:
    raise RuntimeError("Invalid environment variable DB_URI_ASYNC")

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
