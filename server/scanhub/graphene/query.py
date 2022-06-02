import graphene
from datetime import date
from pkg_resources import require
from tortoise.contrib.pydantic import pydantic_model_creator
from scanhub.graphene.random_date import random_date
from scanhub.graphene.types import Patient, PatientSexGQL, PatientStatusGQL, User, Device, Procedure, Recording, Site

from scanhub.database.models import Patient as PatientModel
from scanhub.database.models import Procedures as ProceduresModel
from scanhub.database.models import Recordings as RecordingsModel
from scanhub.database.models import Device as DeviceModel
from scanhub.database.models import Site as SiteModel
from scanhub.database.models import User as UserModel
from scanhub.database.utils import ModelUtilities

model_utils = ModelUtilities()


class Query(graphene.ObjectType):
    # TODO: Util functions may lead to null values in nested database queries!
    # Instead maybe use query class member variables as a return value?

    all_patients = graphene.List(graphene.NonNull(Patient), required=True)
    patient = graphene.Field(Patient, id=graphene.Int(required=True), required=True)
    recording = graphene.Field(Recording, id=graphene.Int(required=True), required=True)
    all_user = graphene.List(graphene.NonNull(User), required=True)
    all_devices = graphene.List(graphene.NonNull(Device), required=True)

    async def resolve_all_patients(root, info):
        patients = await PatientModel.all()
        return [await model_utils.create_patient(id=patient.id) for patient in patients]
        
    async def resolve_patient(self, info, id: int):
        return await model_utils.create_patient(id=id)

    async def resolve_recording(self, info, id: int):
        return await model_utils.create_recording(id=id)    

    async def resolve_all_user(self, info):
        users = await UserModel.all()
        return [await model_utils.create_user(id=user.id) for user in users]

    async def resolve_all_devices(self, info):
        devices = await DeviceModel.all()
        return [await model_utils.create_device(id=device.id) for device in devices]



# class Query(graphene.ObjectType):
#     # This maybe fixes the null value problem? (Does not work yet)

#     all_devices = graphene.List(graphene.NonNull(Device), required=True)

#     device = graphene.Field(Device, id=graphene.Int(required=True), required=True)
#     site = graphene.Field(Site, id=graphene.Int(required=True), required=True)

#     async def resolve_site(self, info, id: int):
#         site = await SiteModel.get(id=id)
#         return Site(
#             id=id,
#             name=site.name,
#             city=site.city,
#             country=site.country,
#             address=site.address
#         )

#     async def resolve_device(self, info, id: int):
#         device = await DeviceModel.get(id=id)
#         return Device(
#             id=device.id,
#             modality=device.modality,
#             address=device.address,
#             created_at=device.created_at,
#             site=self.site(device.site_id)
#         )

#     async def resolve_all_devices(self, info):
#         devices = await DeviceModel.all()
#         return [self.device(dev.id) for dev in devices]