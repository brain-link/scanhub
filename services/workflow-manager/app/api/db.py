import os
import datetime

from sqlalchemy import create_engine, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

# Create base for device
Base = declarative_base()
engine = create_engine(os.getenv('DB_URI'), echo=False)


def init_db() -> None:
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Workflow(Base):
    """
    Device ORM model
    """
    __tablename__ = 'workflow'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    host: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=True)
    # TODO: Use enum to describe workflow modality
    modality: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    # TODO: Use enum to describe workflow status
    status: Mapped[str] = mapped_column(nullable=False)
    kafka_topic: Mapped[str] = mapped_column(nullable=False)

    datetime_created: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    datetime_updated: Mapped[datetime.datetime] = mapped_column(onupdate=func.now(), nullable=True)

    def update(self, data: dict):
        """Update attributes of orm model

        Arguments:
            data {dict} -- Entries to be updated
        """
        for key, value in data.items():
            setattr(self, key, value)


# Create async engine and session, echo=True generates console output
async_engine = create_async_engine(
    os.getenv('DB_URI_ASYNC'), 
    future=True, 
    echo=False,
    isolation_level="AUTOCOMMIT",
)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
