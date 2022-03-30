from dataclasses import dataclass
from unicodedata import name

from tomlkit import comment, date
import graphene

from scanhub.database.enums import PatientSex, PatientStatus


PatientSexGQL = graphene.Enum.from_enum(PatientSex)
PatientStatusGQL = graphene.Enum.from_enum(PatientStatus)


class User(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    age = graphene.Int(required=True)


class Patient(graphene.ObjectType):
    id = graphene.ID(required=True)
    sex = graphene.Field(PatientSexGQL, required=True)
    birthday = graphene.Date(required=True)
    concern = graphene.String(required=True)
    admission_date = graphene.DateTime(required=True)
    status = graphene.Field(PatientStatusGQL, required=True)


class Device(graphene.ObjectType):
    id = graphene.ID(required=True)
    modality = graphene.String(required=True)
    address = graphene.String(required=True)
    created_at = graphene.DateTime(required=True)
    site_id = graphene.ID(required=True)        # is this an ID or: graphene.Field(Site, required=True) ?


class Site(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    city = graphene.String(required=True)
    country = graphene.String(required=True)
    address = graphene.String(required=True)


class Procedure(graphene.ObjectType):
    id = graphene.ID(required=True)
    date = graphene.DateTime(required=True)
    reason = graphene.String(required=True)
    patient_id = graphene.ID(required=True)     # is this an ID or: graphene.Field(Patient, required=True) ?


class Recording(graphene.ObjectType):
    id = graphene.ID(required=True)
    date = graphene.DateTime(required=True)
    thumbnail = graphene.ID(required=False)     # ID to blob storage ?
    comment = graphene.String(required=True)
    data = graphene.ID(required=False)          # ID to blob storage ?
    device_id = graphene.ID(required=True)      # is this an ID or: graphene.Field(Device, required=True) ?
    procedure_id = graphene.ID(required=True)   # is this an ID or: graphene.Field(Procedure, required=True) ?


