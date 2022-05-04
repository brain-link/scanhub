from dataclasses import dataclass
import imp
from typing_extensions import Required
from unicodedata import name

from tomlkit import comment, date
import graphene

from scanhub.database.enums import PatientSex, PatientStatus

from scanhub.database.models import Patient as PatientModel
from scanhub.database.models import Procedures as ProceduresModel
from scanhub.database.models import Device as DeviceModel

PatientSexGQL = graphene.Enum.from_enum(PatientSex)
PatientStatusGQL = graphene.Enum.from_enum(PatientStatus)


class Patient(graphene.ObjectType):
    id = graphene.ID(required=True)
    sex = graphene.Field(PatientSexGQL, required=True)
    birthday = graphene.Date(required=True)
    concern = graphene.String(required=True)
    admission_date = graphene.DateTime(required=True)
    status = graphene.Field(PatientStatusGQL, required=True)

class User(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    patients = graphene.List(graphene.NonNull(Patient), required=False)

class Site(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    city = graphene.String(required=True)
    country = graphene.String(required=True)
    address = graphene.String(required=True)

class Device(graphene.ObjectType):
    id = graphene.ID(required=True)
    modality = graphene.String(required=True)
    address = graphene.String(required=True)
    created_at = graphene.DateTime(required=True)
    site = graphene.Field(Site, required=False)

class Procedure(graphene.ObjectType):
    id = graphene.ID(required=True)
    date = graphene.DateTime(required=True)
    reason = graphene.String(required=True)
    patient_id = graphene.ID(required=True)     # is this an ID or: graphene.Field(Patient, required=True) ?

class Recording(graphene.ObjectType):
    id = graphene.ID(required=True)
    date = graphene.DateTime(required=True)
    thumbnail = graphene.ID(required=False)
    comment = graphene.String(required=False)
    data = graphene.ID(required=False)

    device = graphene.Field(Device, required=False)
    procedure = graphene.Field(Procedure, required=True)