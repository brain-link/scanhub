from typing import Optional
from enum import IntEnum
from pydantic import BaseModel, Extra
from tortoise import models, fields


# Enums
class Modality(IntEnum):
    NONE = 0
    MRI = 1
    ECG = 2
    EEG = 3
    CT = 4


# Models
class Device(models.Model):
    """
    The Device Model
    """
    id = fields.IntField(pk=True, null=False, unique=True)
    modality: Modality = fields.IntEnumField(Modality, null=False)
    address = fields.CharField(max_length=100, null=False)
    site = fields.TextField(null=False)
    registration_date = fields.DatetimeField(auto_now_add=True)

class CreateDevice(BaseModel, extra=Extra.ignore):
    modality: Optional[int] = 0
    address: Optional[str] = "0.0.0.1"



class Workflow(models.Model):
    """
    The Workflow Model
    """
    id = fields.IntField(pk=True, null=False, unique=True)



class Exam(models.Model):
    """
    The Exam Model
    """
    id = fields.IntField(pk=True, null=False, unique=True)
    date = fields.DatetimeField(auto_now_add=True)
    patient = fields.TextField(null=False)
    concern = fields.TextField(null=False)

class CreateExam(BaseModel, extra=Extra.ignore):
    patient: str
    concern: str



class Procedure(models.Model):
    """
    The Procedures model
    """
    id = fields.IntField(pk=True, null=False, unique=True)
    date = fields.DatetimeField(auto_now_add=True)
    exam = fields.ForeignKeyField("models.Exam", related_name="procedure")
    modality = fields.IntEnumField(
        Modality,
        default=Modality.NONE,
        null=False,
    )

class CreateProcedure(BaseModel, extra=Extra.ignore):
    exam_id: int
    modality_id: int



class Record(models.Model):
    """
    The Recordings model
    """
    id = fields.IntField(pk=True, null=False, unique=True)
    date = fields.DatetimeField(auto_now_add=True)
    sequence = fields.IntField(unique=False)
    comment = fields.TextField(null=True)
    device = fields.ForeignKeyField("models.Device", related_name="record")
    procedure = fields.ForeignKeyField("models.Procedure", related_name="record")
    workflow = fields.ForeignKeyField("models.Workflow", related_name="record", null=True)

class Create_Record(BaseModel, extra=Extra.ignore):
    sequence: int
    comment: str
    device_id: int
    procedure_id: int
    workflow_id: Optional[int]
