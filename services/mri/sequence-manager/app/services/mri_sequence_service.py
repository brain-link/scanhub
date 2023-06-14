# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""MRI sequence service."""

import datetime
import logging
from typing import Any, List, Tuple

from bson import ObjectId
from database.models import MRISequence
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)


async def create_mri_sequence(db: AsyncIOMotorDatabase, mri_sequence: MRISequence) -> MRISequence:
    """
    Create a new MRI sequence in the database.

    TODO: Seems like AsyncIOMotorDatabase is invalid.
    Do you mean pymongo.database.Database? -> from pymongo.database import Database
    According to motor documentation it should be Database.
    See: database/mongodb.py, you create db = Database()

    Parameters:
    -----------
    db : AsyncIOMotorDatabase
        The MongoDB database handle.
    mri_sequence : MRISequence
        The MRI sequence data to store.

    Returns:
    --------
    MRISequence
        The created MRI sequence.
    """
    logger.info("create MRI sequence...")

    mri_sequence.created_at = datetime.datetime.utcnow()
    mri_sequence.updated_at = mri_sequence.created_at
    mri_sequence_data = mri_sequence.dict(by_alias=True)

    mri_sequence_data.pop("id", None)  # Remove the id field from the dictionary
    mri_sequence_data.pop("_id", None)  # Remove the id field from the dictionary
    result = await db.collection.insert_one(mri_sequence_data)
    mri_sequence.id = str(result.inserted_id)

    logger.info("done creating MRI sequence.")
    return mri_sequence


async def get_mri_sequences(db: AsyncIOMotorDatabase) -> List[MRISequence]:
    """
    Retrieve all MRI sequences from the database.

    Parameters:
    -----------
    db : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns:
    --------
    List[MRISequence]
        The list of MRI sequences.
    """
    cursor = db.collection.find()
    sequences = []

    async for sequence in cursor:
        sequence["_id"] = str(sequence["_id"])
        sequences.append(MRISequence(**sequence))

    return sequences


async def get_mri_sequence_by_id(db: AsyncIOMotorDatabase, mri_sequence_id: str) -> (MRISequence | None):
    """
    Retrieve an MRI sequence by its ID from the database.

    Parameters:
    -----------
    db : AsyncIOMotorDatabase
        The MongoDB database handle.
    mri_sequence_id : str
        The ID of the MRI sequence to retrieve.

    Returns:
    --------
    MRISequence
        The retrieved MRI sequence.
    """    
    logger.info("retrieve MRI sequence...")
    if (sequence_data := await db.collection.find_one({"_id": ObjectId(mri_sequence_id)})):
        sequence_data["_id"] = str(sequence_data["_id"])  # Convert the ObjectId to a string
        logger.info("done retrieving MRI sequence.")
        return MRISequence(**sequence_data)
    return None


async def update_mri_sequence(db: AsyncIOMotorDatabase, mri_sequence_id: str, mri_sequence: MRISequence) -> (MRISequence | None):
    """
    Update an MRI sequence with new data in the database.

    Parameters:
    -----------
    db : AsyncIOMotorDatabase
        The MongoDB database handle.
    mri_sequence_id : str
        The ID of the MRI sequence to update.
    mri_sequence : MRISequence
        The updated MRI sequence data.

    Returns:
    --------
    MRISequence
        The updated MRI sequence.
    """
    mri_sequence.updated_at = datetime.datetime.utcnow()
    result = await db.collection.replace_one({"_id": mri_sequence_id}, mri_sequence.dict(by_alias=True))

    return mri_sequence if result.modified_count > 0 else None


async def delete_mri_sequence(db: AsyncIOMotorDatabase, mri_sequence_id: str) -> int:
    """
    Delete an MRI sequence by its ID from the database.

    Parameters:
    -----------
    db : AsyncIOMotorDatabase
        The MongoDB database handle.
    mri_sequence_id : str
        The ID of the MRI sequence to delete.

    Returns:
    --------
    int
        The number of deleted MRI sequences (0 or 1).
    """
    result = await db.collection.delete_one({"_id": mri_sequence_id})
    return result.deleted_count


async def search_mri_sequences(db: AsyncIOMotorDatabase, search_query: str) -> List[MRISequence]:
    """
    Search for MRI sequences in the database based on a search query.

    Args:
        db: The MongoDB database.
        search_query: The search query to filter MRI sequences.

    Returns:
        A list of MRISequence objects that match the search query.
    """
    mri_sequences_collection = db.collection
    cursor = mri_sequences_collection.find({"$text": {"$search": search_query}})
    mri_sequences = await cursor.to_list(length=100)

    return mri_sequences


async def download_mri_sequence_file(db: AsyncIOMotorDatabase, mri_sequence_id: str) -> Tuple[str, Any]:
    """
    Download the MRI sequence file associated with the given MRI sequence ID.

    Args:
        db: The MongoDB database.
        mri_sequence_id: The ID of the MRI sequence.

    Returns:
        A tuple containing the file name and the file content or reference.
    """
    # Retrieve the MRI sequence document from the database
    mri_sequence_collection = db.collection
    mri_sequence = await mri_sequence_collection.find_one({"_id": ObjectId(mri_sequence_id)})

    # Check if the MRI sequence exists
    if not mri_sequence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MRI sequence not found")

    # Extract the file name and the file content
    file_name = f"{mri_sequence_id}.nii.gz"  # or use mri_sequence['file_name'] if it's stored in the database
    file_content = mri_sequence["file"]

    return file_name, file_content
