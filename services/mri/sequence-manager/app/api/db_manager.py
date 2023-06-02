# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Database manager file for the MRI sequence manager service."""

from api.models import SequenceIn, SequenceOut, SequenceUpdate
from api.db import sequences, database


async def add_sequence(payload: SequenceIn):
    query = sequences.insert().values(**payload.dict())

    return await database.execute(query=query)

async def get_all_sequences():
    query = sequences.select()
    return await database.fetch_all(query=query)

async def get_sequence(id):
    query = sequences.select(sequences.c.id==id)
    return await database.fetch_one(query=query)

async def delete_sequence(id: int):
    query = sequences.delete().where(sequences.c.id==id)
    return await database.execute(query=query)

async def update_sequence(id: int, payload: SequenceIn):
    query = (
        sequences
        .update()
        .where(sequences.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)