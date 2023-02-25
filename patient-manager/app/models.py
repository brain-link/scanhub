from datetime import datetime
from lib2to3.pytree import Base
from typing import Optional
import pydantic
from tortoise import models, fields
from app.enums import PatientStatus, PatientSex, Modality
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, Extra

class Device(models.Model):
    """
    The Device model
    """
    id = fields.IntField(pk=True, null=False, unique=True)
    modality: Modality = fields.IntEnumField(Modality, null=False)
    address = fields.CharField(max_length=100, null=False)
    site = fields.ForeignKeyField("models.Site", related_name="device")
    created_at = fields.DatetimeField(auto_now_add=True)

class CreateDevice(BaseModel, extra=Extra.ignore):
    modality: Optional[int] = 0
    address: Optional[str] = "0.0.0.1"

class Patient(models.Model):
    """
    The Patient model
    """
    id = fields.IntField(pk=True, null=False, unique=True)
    sex: PatientSex = fields.IntEnumField(
        PatientSex, default=PatientSex.NONE, null=False)
    birthday = fields.TextField(null=False) # fields.DateField(null=False)
    concern = fields.TextField(null=False)
    admission_date = fields.DatetimeField(auto_now_add=True, null=False)
    status: PatientStatus = fields.IntEnumField(
        PatientStatus, default=PatientStatus.NEW, null=False)

class CreatePatient(BaseModel, extra=Extra.ignore):
    sex: int
    birthday: str
    concern: str


class Procedures(models.Model):
    """
    The Procedures model
    """
    id = fields.IntField(pk=True, null=False, unique=True)
    date = fields.DatetimeField(auto_now_add=True)
    reason = fields.TextField(null=False)
    patient = fields.ForeignKeyField(
        "models.Patient", related_name="procedures")

class CreateProcedure(BaseModel, extra=Extra.ignore):
    reason: str
    patient_id: int


class Recordings(models.Model):
    """
    The Recordings model
    """
    id = fields.IntField(pk=True, null=False, unique=True)
    date = fields.DatetimeField(auto_now_add=True)
    thumbnail = fields.BinaryField(null=True)
    comment = fields.TextField(null=True)
    data = fields.TextField(null=True)  # fields.BinaryField(null=True)
    
    device = fields.ForeignKeyField(
        "models.Device", related_name="recordings")
    procedure = fields.ForeignKeyField(
        "models.Procedures", related_name="recordings")

class Create_Record(BaseModel, extra=Extra.ignore):
    comment: str
    device_id: int
    procedure_id: int
    data: str   # Optional[bytes] = bytes() # Optional[str] = ""
    thumbnail: Optional[bytes] = bytes()

class Site(models.Model):
    """
    The Site model
    """
    id = fields.IntField(pk=True, null=False, unique=True)
    name = fields.CharField(max_length=1000, null=False)
    city = fields.CharField(max_length=1000, null=False)
    country = fields.CharField(max_length=1000, null=False)
    address = fields.CharField(max_length=1000, null=False)
    patients = fields.ManyToManyField(
        "models.Patient", related_name="site", through="Site_Patient")
    users = fields.ManyToManyField(
        "models.User", related_name="site", through="Site_User")

class CreateSite(BaseModel, extra=Extra.ignore):
    name: str
    city: str
    country: str
    address: str

class User(models.Model):
    """
    The User model
    """
    # from core_apis.models.AbstractAdmin
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=200)
    # User
    last_login = fields.DatetimeField(
        description="Last Login", default=datetime.now)
    email = fields.CharField(max_length=200, default="")
    avatar = fields.CharField(max_length=200, default="")
    intro = fields.TextField(default="")
    created_at = fields.DatetimeField(auto_now_add=True)
    patients = fields.ManyToManyField(
        "models.Patient", related_name="user", through="User_Patient")

    def __str__(self):
        return f"{self.pk}#{self.username}"


class Config(models.Model):
    label = fields.CharField(max_length=200)
    key = fields.CharField(max_length=20, unique=True,
                           description="Unique key for config")
    value = fields.JSONField()
    status: PatientStatus = fields.IntEnumField(
        PatientStatus, default=PatientStatus.NEW)


class Status(BaseModel):
    message: str