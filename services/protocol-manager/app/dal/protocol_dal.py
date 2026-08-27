# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Data access layer (DAL) between fastapi endpoint and sql database."""

from pprint import pprint
from uuid import UUID

from scanhub_libraries.models import BaseProtocol
from sqlalchemy.engine import Result
from sqlalchemy.future import select

from app.db.postgres import (
    Protocol,
    async_session,
)


async def add_protocol_data(payload: BaseProtocol, creator: str) -> Protocol:
    """Create new protocol."""
    new_protocol = Protocol(**payload.model_dump(), creator=creator)
    async with async_session() as session:
        session.add(new_protocol)
        await session.commit()
        await session.refresh(new_protocol)
    print("***** NEW PROTOCOL *****")
    pprint(new_protocol.__dict__)
    return new_protocol


async def get_protocol_data(protocol_id: UUID) -> Protocol | None:
    """Get protocol by id."""
    async with async_session() as session:
        protocol = await session.get(Protocol, protocol_id)
    return protocol


async def get_all_protocol_data(patient_id: UUID) -> list[Protocol]:
    """Get all protocols assigned to a certain patient."""
    async with async_session() as session:
        result: Result = await session.execute(select(Protocol).where(Protocol.patient_id == patient_id))
        protocols = list(result.scalars().all())
    return protocols


async def get_all_protocol_template_data() -> list[Protocol]:
    """Get all protocol templates."""
    async with async_session() as session:
        result: Result = await session.execute(select(Protocol).where(Protocol.is_template))
        protocols = list(result.scalars().all())
    return protocols


async def delete_protocol_data(protocol_id: UUID) -> bool:
    """Delete protocol by id. Also deletes associated tasks."""
    async with async_session() as session:
        if protocol := await session.get(Protocol, protocol_id):
            for task in protocol.tasks:
                await session.delete(task)
            await session.delete(protocol)
            await session.commit()
            return True
        return False


async def update_protocol_data(protocol_id: UUID, payload: BaseProtocol) -> Protocol | None:
    """Update existing protocol entry."""
    async with async_session() as session:
        if protocol := await session.get(Protocol, protocol_id):
            protocol.update(payload)
            await session.commit()
            await session.refresh(protocol)
            return protocol
        return None
