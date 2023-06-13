# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""MRI sequence endpoints"""

import json
import tempfile
import os
from pathlib import Path
import logging

from fastapi import (
    APIRouter,
    Depends,
    Form,
    status,
    HTTPException,
    File,
    UploadFile,
    BackgroundTasks
)
from os.path import exists
from fastapi.responses import FileResponse
from pypulseq import Sequence
import plotly
from services.mri_sequence_plot import get_sequence_plot
from typing import Union
from motor.motor_asyncio import AsyncIOMotorDatabase
from dependencies import get_database
from database.models import MRISequence, MRISequenceCreate
from services import (
    create_mri_sequence,
    get_mri_sequences,
    get_mri_sequence_by_id,
    delete_mri_sequence,
    update_mri_sequence,
    search_mri_sequences,
    download_mri_sequence_file,
)

from bson.binary import Binary

logger = logging.getLogger(__name__)

async def mri_sequence_form(
    name: str = Form(...),
    description: str = Form(None),
    sequence_type: str = Form(None),
    tags: str = Form(None)) -> MRISequenceCreate:
    """
    Convert the form data to an MRISequenceCreate object.
    
    Parameters:
    -----------
    name : str
        The name of the MRI sequence.
    description : str
        The description of the MRI sequence.
    sequence_type : str
        The type of the MRI sequence.
    tags : str
        The tags of the MRI sequence.
    
    Returns:
    --------
    MRISequenceCreate
        The MRI sequence data.
    """
    tags_list = json.loads(tags) if tags else []
    return MRISequenceCreate(
        name=name,
        description=description,
        sequence_type=sequence_type,
        tags=tags_list
    )

router = APIRouter()

@router.post("/", response_model=MRISequence, status_code=status.HTTP_201_CREATED)
async def create_mri_sequence_endpoint(mri_sequence: MRISequence, db=Depends(get_database)):
    """
    Create a new MRI sequence and store it in the database.

    Parameters:
    -----------
    mri_sequence : MRISequence
        The MRI sequence data to store.
    db : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns:
    --------
    MRISequence
        The created MRI sequence.
    """
    logger.info(f"Creating MRI sequence with data: %s", mri_sequence)
    return await create_mri_sequence(db, mri_sequence)

@router.post("/upload", response_model=MRISequence, status_code=status.HTTP_201_CREATED)
async def upload_mri_sequence_file(mri_sequence: MRISequenceCreate = Depends(mri_sequence_form),
                                   file: UploadFile=File(...),
                                   db=Depends(get_database)
                                   ):
    """
    Upload an MRI sequence file and store it with the provided metadata.

    Parameters:
    -----------
    mri_sequence : MRISequenceCreate
        The MRI sequence metadata.
    file : UploadFile
        The MRI sequence file to store.
    db : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns:
    --------
    MRISequence
        The stored MRI sequence with the uploaded file.
    """
    logger.info(f"Uploading MRI sequence file with metadata: %s", mri_sequence)

    filename = file.filename
    file_extension = Path(filename).suffix

    # Read the content of the uploaded file
    file_content = await file.read()

    # Convert the MRISequenceCreate object to an MRISequence object
    mri_sequence_with_file = MRISequence(**mri_sequence.dict(), file=Binary(file_content))
    mri_sequence_with_file.file_extension = file_extension

    # Store the MRI sequence with the uploaded file in the database
    return await create_mri_sequence(db, mri_sequence_with_file)


@router.get("/", response_model=list[MRISequence])
async def get_mri_sequences_endpoint(db=Depends(get_database)):
    """
    Retrieve a list of all MRI sequences from the database.

    Parameters:
    -----------
    db : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns:
    --------
    List[MRISequence]
        The list of MRI sequences.
    """
    logger.info("Retrieving all MRI sequences")
    return await get_mri_sequences(db)


@router.get("/{mri_sequence_id}", response_model=MRISequence)
async def get_mri_sequence_by_id_endpoint(mri_sequence_id: str, db=Depends(get_database)):
    """
    Retrieve an MRI sequence by its ID.

    Parameters:
    -----------
    mri_sequence_id : str
        The ID of the MRI sequence to retrieve.
    db : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns:
    --------
    MRISequence
        The retrieved MRI sequence.
    """
    logger.info(f"Retrieving MRI sequence with ID: %s", mri_sequence_id)
    mri_sequence = await get_mri_sequence_by_id(db, mri_sequence_id)
    if mri_sequence:
        return mri_sequence
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MRI sequence not found")
    

@router.get("/mri-sequence-file/{mri_sequence_id}")
async def get_mri_sequence_file_by_id_endpoint(mri_sequence_id: str, background_tasks: BackgroundTasks, name: str = "sequence", db=Depends(get_database)):
    """
    Retrieve an MRI sequence file by its ID.

    Parameters:
    -----------
    mri_sequence_id : str
        The ID of the MRI sequence to retrieve.
    background_tasks : BackgroundTasks
        The background tasks to run.
    name : str
        The name of the file to download.
    db : AsyncIOMotorDatabase
        The MongoDB database handle.
    
    Returns:
    --------
    FileResponse
        The retrieved MRI sequence file.
    """
    
    logger.info(f"Retrieving MRI sequence file with ID: %s", mri_sequence_id)
    mri_sequence = await get_mri_sequence_by_id(db, mri_sequence_id)
    
    if mri_sequence:
        binary_data = mri_sequence.file
        file_extension = mri_sequence.file_extension

        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(binary_data)
        temp_file.close()

        # Create a FileResponse with the temporary file and the retrieved file extension
        response = FileResponse(
            temp_file.name,
            media_type="application/octet-stream",
            filename=f"{name}{file_extension}",  # Use the retrieved file extension
            headers={"Content-Disposition": f"attachment; filename={name}{file_extension}"},  
        )

        # Function to delete the temporary file
        def delete_temp_file(file_path: str):
            os.unlink(file_path)
        
        # Add the background task to delete the temporary file
        background_tasks.add_task(delete_temp_file, temp_file.name)

        return response

    raise HTTPException(status_code=404, detail="Binary data not found")


@router.put("/{mri_sequence_id}", response_model=MRISequence)
async def update_mri_sequence_endpoint(mri_sequence_id: str, mri_sequence: MRISequence, db=Depends(get_database)):
    """
    Update an MRI sequence with new data.

    Parameters:
    -----------
    mri_sequence_id : str
        The ID of the MRI sequence to update.
    mri_sequence : MRISequence
        The updated MRI sequence data.
    db : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns:
    --------
    MRISequence
        The updated MRI sequence.
    """
    logger.info(f"Updating MRI sequence with ID: %s", mri_sequence_id)
    updated_mri_sequence = await update_mri_sequence(db, mri_sequence_id, mri_sequence)
    if updated_mri_sequence:
        return updated_mri_sequence
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MRI sequence not found")


@router.delete("/{mri_sequence_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mri_sequence_endpoint(mri_sequence_id: str, db=Depends(get_database)):
    """
    Delete an MRI sequence by its ID.

    Parameters:
    -----------
    mri_sequence_id : str
        The ID of the MRI sequence to delete.
    db : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns:
    --------
    None
    """
    logger.info(f"Deleting MRI sequence with ID: %s", mri_sequence_id)
    deleted_count = await delete_mri_sequence(db, mri_sequence_id)
    if deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MRI sequence not found")


@router.get("/mri-sequence-plot/{seq_id}", status_code=status.HTTP_201_CREATED)
async def plot_mri_sequence(seq_id: str, db=Depends(get_database)) -> str:
    """Generate plotly sequence plot data.

    Parameters
    ----------
    seq_id
        Id of the sequence to be plotted

    Returns
    -------
        List of plot data models for plotly
    """
    filename = f"data_lake/mri-sequence-{seq_id}"

    # Check if pulseq file already exist, request it from db if not
    if not exists(filename+".seq"):
        if (mri_seq := await get_mri_sequence_by_id(db, seq_id)):

            with open(filename+".seq", "w") as fh:
                fh.write(mri_seq.file.decode("utf-8"))
            print("WRITTEN PULSEQ FILE")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # Generate plotly json string from sequence object, if json file does not already exists
    if not exists(filename+".json"):
        seq = Sequence()
        seq.read(filename+".seq")

        fig = get_sequence_plot(seq)
        plot_data = plotly.io.to_json(fig, pretty=True)

        with open(filename+".json", "w") as fh:
            fh.write(plot_data)
    else:
        with open(filename+".json") as fh:
            plot_data = json.dumps(json.loads(fh.read()), indent=2)

    # print(plot_data)

    return plot_data
