from datetime import datetime
from lib2to3.pytree import Base
from typing import Optional
import pydantic
from tortoise import models, fields
from scanhub.enums import PatientStatus, PatientSex, Modality
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


class Patient(models.Model):
    """
    The Patient model
    """
    id = fields.IntField(pk=True, null=False, unique=True)
    sex: PatientSex = fields.IntEnumField(
        PatientSex, default=PatientSex.NONE, null=False)
    birthday = fields.DateField(null=False)
    concern = fields.TextField(null=False)
    admission_date = fields.DatetimeField(auto_now_add=True, null=False)
    status: PatientStatus = fields.IntEnumField(
        PatientStatus, default=PatientStatus.NEW, null=False)

class CreatePatient(BaseModel, extra=Extra.ignore):
    sex: int
    birthday: str
    concern: str
    admission_date: str
    status = int


class Procedures(models.Model):
    """
    The Procedures model
    """
    id = fields.IntField(pk=True, null=False, unique=True)
    date = fields.DatetimeField(null=False)
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
    data = fields.BinaryField(null=True)
    
    device = fields.ForeignKeyField(
        "models.Device", related_name="recordings")
    procedure = fields.ForeignKeyField(
        "models.Procedures", related_name="recordings")

class Create_Record(BaseModel, extra=Extra.ignore):
    comment: str
    device_id: int
    procedure_id: int
    thumbnail: Optional[bytes] = bytes()
    data: Optional[bytes] = bytes()


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
