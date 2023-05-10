from pydantic import BaseModel, Field
from typing import List, Optional, Any
import datetime

class MRISequence(BaseModel):
    """
    A class representing an MRI sequence definition file and its associated metadata.

    Attributes:
        id: The unique identifier for the MRI sequence, autogenerated by MongoDB.
        name: The name of the MRI sequence.
        description: A brief description of the MRI sequence.
        sequence_type: The type of MRI sequence, such as T1-weighted, T2-weighted, etc.
        created_at: The timestamp of when the MRI sequence was created.
        updated_at: The timestamp of when the MRI sequence was last updated.
        tags: A list of tags or keywords associated with the MRI sequence, useful for searching and filtering.
        file: The MRI sequence definition file content or a reference to the stored file, such as a GridFS identifier or an S3 URL.
        file_extension: The file extension of the MRI sequence definition file.
    """
    id: Optional[str] = Field(alias="_id")
    name: str
    description: Optional[str]
    sequence_type: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    tags: Optional[List[str]]
    file: Optional[Any]
    file_extension: Optional[str]

class MRISequenceCreate(BaseModel):
    """
    A class representing an MRI sequence definition file and its associated metadata.

    Attributes:
        id: The unique identifier for the MRI sequence, autogenerated by MongoDB.
        name: The name of the MRI sequence.
        description: A brief description of the MRI sequence.
        sequence_type: The type of MRI sequence, such as T1-weighted, T2-weighted, etc.
        created_at: The timestamp of when the MRI sequence was created.
        updated_at: The timestamp of when the MRI sequence was last updated.
        tags: A list of tags or keywords associated with the MRI sequence, useful for searching and filtering.
    """
    id: Optional[str] = Field(alias="_id")
    name: str
    description: Optional[str]
    sequence_type: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    tags: Optional[List[str]]
