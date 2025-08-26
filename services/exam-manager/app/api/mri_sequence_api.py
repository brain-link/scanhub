# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""MRI sequence endpoints."""

import datetime
import os
import tempfile
from pathlib import Path

from bson import ObjectId
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
from scanhub_libraries.models import BaseMRISequence, MRISequenceOut
from scanhub_libraries.security import get_current_user

# from app.dal import mri_sequence_dal
from app.db.mongodb import get_mongo_database

seq_router = APIRouter(dependencies=[Depends(get_current_user)])


async def mri_sequence_form(
    name: str = Form(...),
    description: str = Form(""),
    sequence_type: str = Form(""),
    tags: list[str] = Form([]),
) -> BaseMRISequence:
    """Convert form data to BaseMRISequence model.

    Parameters
    ----------
    name : str
        The name of the MRI sequence.
    description : str | None
        A description of the MRI sequence.
    sequence_type : str | None
        The type of the MRI sequence (e.g., "imaging", "calibration", etc.).
    tags : list[str]
        A list of tags associated with the MRI sequence.
    """
    return BaseMRISequence(
        name=name,
        description=description,
        sequence_type=sequence_type,
        tags=tags,
    )


@seq_router.get("/sequence/{sequence_id}", response_model=MRISequenceOut, tags=["mri sequences"])
async def get_mri_sequence_by_id(
    sequence_id: str,
    database=Depends(get_mongo_database),
) -> MRISequenceOut:
    """Retrieve an MRI sequence by its ID.

    Parameters
    ----------
    sequence_id : str
        The ID of the MRI sequence to retrieve.
    database : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns
    -------
    MRISequence
        The retrieved MRI sequence.
    """
    if sequence := await database.collection.find_one({"_id": ObjectId(sequence_id)}):
        sequence["_id"] = str(sequence["_id"])  # Convert ObjectId to str
        return MRISequenceOut(**sequence)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"MRI sequence with ID {sequence_id} not found.")


@seq_router.post(
    "/sequence",
    response_model=MRISequenceOut,
    status_code=status.HTTP_201_CREATED,
    tags=["mri sequences"],
)
async def create_mri_sequence(
    sequence_meta: BaseMRISequence = Depends(mri_sequence_form),
    seq_file: UploadFile = File(...),
    xml_file: UploadFile | None = None,
    database=Depends(get_mongo_database),
):
    """Upload an MRI sequence file and store it with the provided metadata.

    Parameters
    ----------
    mri_sequence : MRISequenceCreate
        The MRI sequence metadata.
    seq_file : UploadFile
        The MRI sequence file to store.
    xml_file : UploadFile
        The ISMRMRD header xml file to store.
    database : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns
    -------
    MRISequence
        The stored MRI sequence with the uploaded file.
    """
    # Check sequence file
    if seq_filename := seq_file.filename:
        seq_file_suffix = Path(seq_filename).suffix
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid sequence file",
        )

    payload = sequence_meta.model_dump(by_alias=True)
    payload["created_at"] = datetime.datetime.now(datetime.timezone.utc)

    # Read the content of the uploaded sequence file
    payload["seq_file"] = Binary(await seq_file.read())
    payload["seq_file_extension"] = seq_file_suffix

    # Check xml file
    if xml_file is not None:
        if xml_filename := xml_file.filename:
            xml_file_suffix = Path(xml_filename).suffix
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid header file",
            )
        # Read the content of the uploaded header file
        payload["xml_file"] = Binary(await xml_file.read())
        payload["xml_file_extension"] = xml_file_suffix

    print(f"SEQUENCE OUT PAYLOAD: {payload}")

    if not (result := await database.collection.insert_one(payload)):
        raise HTTPException(status_code=500, detail="Failed to insert sequence.")

    return await get_mri_sequence_by_id(result.inserted_id, database)


@seq_router.get(
    "/sequences/all",
    response_model=list[MRISequenceOut],
    tags=["mri sequences"],
)
async def get_all_mri_sequences(database=Depends(get_mongo_database)):
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
    cursor = database.collection.find()
    sequences = []
    async for seq in cursor:
        seq_dict = {**seq, "_id": str(seq["_id"])}
        sequences.append(MRISequenceOut(**seq_dict))
    return sequences


@seq_router.get("/sequence/{sequence_id}/file", tags=["mri sequences"])
async def get_mri_sequence_file_by_id(
    sequence_id: str,
    background_tasks: BackgroundTasks,
    name: str = "sequence",
    database=Depends(get_mongo_database),
):
    """Retrieve an MRI sequence file by its ID.

    Parameters
    ----------
    sequence_id : str
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
    if mri_sequence := await get_mri_sequence_by_id(sequence_id, database):
        binary_data = mri_sequence.seq_file
        file_extension = mri_sequence.seq_file_extension

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(binary_data)

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


@seq_router.get("/sequence/{sequence_id}/header", tags=["mri sequences"])
async def get_mri_sequence_header_file_by_id(
    sequence_id: str,
    background_tasks: BackgroundTasks,
    name: str = "header",
    database=Depends(get_mongo_database),
):
    """Retrieve an MRI sequence header (ISMRMRD header) file by its ID.

    Parameters
    ----------
    sequence_id : str
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
    if mri_sequence := await get_mri_sequence_by_id(sequence_id, database):
        binary_data = mri_sequence.xml_file
        file_extension = mri_sequence.xml_file_extension

        if binary_data is None or file_extension is None:
            raise HTTPException(status_code=404, detail="No MRD header available")

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(binary_data)

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


@seq_router.put(
    "/sequence/{sequence_id}",
    response_model=MRISequenceOut,
    tags=["mri sequences"],
)
async def update_mri_sequence_endpoint(
    sequence_id: str,
    sequence_meta: BaseMRISequence,
    database=Depends(get_mongo_database),
):
    """Update an MRI sequence with new data.

    Parameters
    ----------
    sequence_id : str
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
    update_fields = {k: v for k, v in sequence_meta.dict(by_alias=True).items() if v and v is not None}
    update_fields["updated_at"] = datetime.datetime.now(datetime.timezone.utc)
    result = await database.collection.update_one({"_id": ObjectId(sequence_id)}, {"$set": update_fields})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MRI sequence not found.")
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update sequence.")
    return await get_mri_sequence_by_id(sequence_id, database)


@seq_router.delete(
    "/sequence/{sequence_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["mri sequences"],
)
async def delete_mri_sequence_endpoint(
    sequence_id: str,
    database=Depends(get_mongo_database),
) -> None:
    """Delete an MRI sequence by its ID.

    Parameters
    ----------
    sequence_id : str
        The ID of the MRI sequence to delete.
    database : AsyncIOMotorDatabase
        The MongoDB database handle.

    Returns
    -------
    None
    """
    # deleted_count = await mri_sequence_dal.delete_mri_sequence(database, sequence_id)
    result = await database.collection.delete_one({"_id": ObjectId(sequence_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MRI sequence not found")


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
