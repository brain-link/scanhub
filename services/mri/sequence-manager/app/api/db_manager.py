#!/usr/bin/env python3

# Project: ScanHub
# File: db_manager.py
# Date: June 2023
#
# License:
# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
#
# SPDX-License-Identifier: GPL-3.0-only OR ScanHub commercial license
#
# Licensees holding valid ScanHub commercial licenses may use this file in
# accordance with the ScanHub Commercial License Agreement provided with the
# Software or, alternatively, in accordance with the GPL-3.0-only as published
# by the Free Software Foundation. Please refer to the License for the
# specific language governing the rights and limitations under either license.
#
# Brief: Database manager file for the MRI sequence manager service.

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