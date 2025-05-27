# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""MRI sequence endpoints."""


import os
import tempfile
from pathlib import Path

from bson.binary import Binary
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from scanhub_libraries.models import MRISequence, MRISequenceCreate
from scanhub_libraries.security import get_current_user

from app.dal import mri_sequence_dal
from app.db.mongodb import get_mongo_database

seq_router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

async def mri_sequence_form(
    name: str = Form(...),
    description: str = Form(None),
    sequence_type: str = Form(None),
    tags: list[str] = Form([]),
) -> MRISequenceCreate:
    """Convert the form data to an MRISequenceCreate object.

    Parameters
    ----------
    name : str
        The name of the MRI sequence.
    description : str
        The description of the MRI sequence.
    sequence_type : str
        The type of the MRI sequence.
    tags : str
        The tags of the MRI sequence.

    Returns
    -------
    MRISequenceCreate
        The MRI sequence data.
    """
    return MRISequenceCreate(
        name=name,
        description=description,
        sequence_type=sequence_type,
        tags=tags,
    )


@seq_router.post("/", response_model=MRISequence, status_code=status.HTTP_201_CREATED, tags=["mri sequences"])
async def upload_mri_sequence_file(
    mri_sequence: MRISequenceCreate = Depends(mri_sequence_form),
    file: UploadFile = File(...),
    database=Depends(get_mongo_database),
):
    """Upload an MRI sequence file and store it with the provided metadata.

    Parameters
    ----------
    mri_sequence : MRISequenceCreate
        The MRI sequence metadata.
    file : UploadFile
        The MRI sequence file to store.
    database : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns
    -------
    MRISequence
        The stored MRI sequence with the uploaded file.
    """
    if filename := file.filename:
        file_extension = Path(filename).suffix
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid sequence file extension",
        )

    # Read the content of the uploaded file
    file_content = await file.read()

    # Convert the MRISequenceCreate object to an MRISequence object
    mri_sequence_with_file = MRISequence(
        **mri_sequence.dict(), file=Binary(file_content)
    )
    mri_sequence_with_file.file_extension = file_extension

    # Store the MRI sequence with the uploaded file in the database
    return await mri_sequence_dal.create_mri_sequence(database, mri_sequence_with_file)


@seq_router.get("/", response_model=list[MRISequence], tags=["mri sequences"],)
async def get_mri_sequences_endpoint(database=Depends(get_mongo_database)):
    """Retrieve a list of all MRI sequences from the database.

    Parameters
    ----------
    database : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns
    -------
    List[MRISequence]
        The list of MRI sequences.
    """
    if not (sequences := await mri_sequence_dal.get_mri_sequences(database)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No sequences found."
        )
    return sequences


@seq_router.get("/{mri_sequence_id}", response_model=MRISequence, tags=["mri sequences"])
async def get_mri_sequence_by_id_endpoint(
    mri_sequence_id: str, database=Depends(get_mongo_database)
):
    """Retrieve an MRI sequence by its ID.

    Parameters
    ----------
    mri_sequence_id : str
        The ID of the MRI sequence to retrieve.
    database : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns
    -------
    MRISequence
        The retrieved MRI sequence.
    """
    if not (mri_sequence := await mri_sequence_dal.get_mri_sequence_by_id(database, mri_sequence_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MRI sequence not found"
        )
    return mri_sequence


@seq_router.get("/mri-sequence-file/{mri_sequence_id}", tags=["mri sequences"])
async def get_mri_sequence_file_by_id_endpoint(
    mri_sequence_id: str,
    background_tasks: BackgroundTasks,
    name: str = "sequence",
    database=Depends(get_mongo_database),
):
    """Retrieve an MRI sequence file by its ID.

    Parameters
    ----------
    mri_sequence_id : str
        The ID of the MRI sequence to retrieve.
    background_tasks : BackgroundTasks
        The background tasks to run.
    name : str
        The name of the file to download.
    database : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns
    -------
    FileResponse
        The retrieved MRI sequence file.
    """
    mri_sequence = await mri_sequence_dal.get_mri_sequence_by_id(database, mri_sequence_id)

    if mri_sequence:
        binary_data = mri_sequence.file
        file_extension = mri_sequence.file_extension

        # Create a temporary file
        # temp_file = tempfile.NamedTemporaryFile(delete=False)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(binary_data)
        # temp_file.close()

        # Create a FileResponse with the temporary file and the retrieved file extension
        response = FileResponse(
            temp_file.name,
            media_type="application/octet-stream",
            filename=f"{name}{file_extension}",  # Use the retrieved file extension
            headers={
                "Content-Disposition": f"attachment; filename={name}{file_extension}"
            },
        )

        # Function to delete the temporary file
        def delete_temp_file(file_path: str):
            os.unlink(file_path)

        # Add the background task to delete the temporary file
        background_tasks.add_task(delete_temp_file, temp_file.name)

        return response

    raise HTTPException(status_code=404, detail="Binary data not found")


@seq_router.put("/{mri_sequence_id}", response_model=MRISequence, tags=["mri sequences"],)
async def update_mri_sequence_endpoint(
    mri_sequence_id: str, mri_sequence: MRISequence, database=Depends(get_mongo_database)
):
    """Update an MRI sequence with new data.

    Parameters
    ----------
    mri_sequence_id : str
        The ID of the MRI sequence to update.
    mri_sequence : MRISequence
        The updated MRI sequence data.
    database : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns
    -------
    MRISequence
        The updated MRI sequence.
    """
    if not (
        updated_mri_sequence := await mri_sequence_dal.update_mri_sequence(
            database, mri_sequence_id, mri_sequence
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MRI sequence not found"
        )
    return updated_mri_sequence


@seq_router.delete("/{mri_sequence_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["mri sequences"],)
async def delete_mri_sequence_endpoint(
    mri_sequence_id: str, database=Depends(get_mongo_database)
):
    """Delete an MRI sequence by its ID.

    Parameters
    ----------
    mri_sequence_id : str
        The ID of the MRI sequence to delete.
    database : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns
    -------
    None
    """
    deleted_count = await mri_sequence_dal.delete_mri_sequence(database, mri_sequence_id)
    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="MRI sequence not found"
        )


# @seq_router.get("/mri-sequence-plot/{seq_id}", tags=["mri sequences"],)
# async def plot_mri_sequence(seq_id: str, database=Depends(get_mongo_database)) -> str:
#     """Generate plotly sequence plot data.

#     Parameters
#     ----------
#     seq_id
#         Id of the sequence to be plotted

#     Returns
#     -------
#         List of plot data models for plotly
#     """
#     filename = f"data_lake/mri-sequence-{seq_id}"

#     # Check if pulseq file already exist, request it from database if not
#     if not exists(filename + ".seq"):
#         if mri_seq := await mri_sequence_dal.get_mri_sequence_by_id(database, seq_id):
#             with open(filename + ".seq", mode="w", encoding="utf8") as file_handle:
#                 file_handle.write(mri_seq.file.decode("utf-8"))
#             print("WRITTEN PULSEQ FILE")
#         else:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#     # Generate plotly json string from sequence object, if json file does not already exists
#     if not exists(filename + ".json"):
#         seq = Sequence()
#         try:
#             seq.read(filename + ".seq")
#         except Exception as exc:
#             print(
#                 "Could not read pulseq file. The uploaded pulseq file is probably not compatible."
#             )
#             raise HTTPException(
#                 status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
#             ) from exc

#         fig = get_sequence_plot(seq)
#         plot_data = plotly.io.to_json(fig, pretty=True)

#         with open(filename + ".json", mode="w", encoding="utf8") as file_handle:
#             file_handle.write(plot_data)
#     else:
#         with open(filename + ".json", mode="r", encoding="utf8") as file_handle:
#             plot_data = json.dumps(json.loads(file_handle.read()), indent=2)

#     return plot_data


# @seq_router.get("/{sequence_id}/plot", response_class=FileResponse, tags=["mri sequences"])
# async def get_sequence_plot(
#     sequence_id: str,
#     database=Depends(get_mongo_database),
# ):
#     """
#     Generate and return a plot of the MRI sequence.

#     Parameters
#     ----------
#     sequence_id : str
#         The ID of the sequence in the database.

#     Returns
#     -------
#     FileResponse
#         The PNG image of the plotted sequence.
#     """
#     sequence: MRISequence = await mri_sequence_dal.get_mri_sequence_by_id(database, sequence_id)

#     if not (sequence or sequence.file):
#         raise HTTPException(status_code=404, detail="Sequence not found or has no file")

#     # Write the binary file to a temporary file
#     with NamedTemporaryFile(suffix=".seq", delete=False) as temp_seq_file:
#         temp_seq_file.write(sequence.file)
#         temp_seq_path = temp_seq_file.name

#     # Read and plot the sequence
#     try:
#         seq = Sequence()
#         seq.read(temp_seq_path)
#         seq.plot(save=True)

#     finally:
#         os.remove(temp_seq_path)  # Clean up the .seq file

#     return FileResponse("seq_plot1.jpg", media_type="image/jpg", filename="sequence_plot_adc.jpg")
#     # return FileResponse("seq_plot2.jpg", media_type="image/jpg", filename="sequence_plot_grad.jpg")
