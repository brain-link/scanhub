import imp
import graphene
from datetime import date
from tortoise.contrib.pydantic import pydantic_model_creator
from scanhub.graphene.random_date import random_date
from scanhub.graphene.types import Patient, PatientSexGQL, PatientStatusGQL, User, Device, Procedure, Recording, Site

from scanhub.database.models import Patient as PatientModel
from scanhub.database.models import User as UserModel

from scanhub.database.utils import ModelUtilities

model_utils = ModelUtilities()


class Query(graphene.ObjectType):
    all_patients = graphene.List(graphene.NonNull(Patient), required=True)
    patient = graphene.Field(Patient, id=graphene.Int(required=True), required=True)
    recording = graphene.Field(Recording, id=graphene.Int(required=True), required=True)
    all_user = graphene.List(graphene.NonNull(User), required=True) 

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