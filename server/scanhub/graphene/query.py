import graphene
from datetime import date
from tortoise.contrib.pydantic import pydantic_model_creator
from scanhub.graphene.random_date import random_date
from scanhub.graphene.types import Patient, PatientSexGQL, PatientStatusGQL, User, Device, Procedure, Recording, Site
from scanhub.database.models import PatientModel, ProceduresModel

patient_pydantic = pydantic_model_creator(PatientModel)

class Query(graphene.ObjectType):
    me = graphene.Field(User)
    all_patients = graphene.List(graphene.NonNull(Patient), required=True)
    get_patient = graphene.Field(Patient, id=graphene.Int(required=True), required=True)

    def resolve_me(root, info):
        return dict(
            id="username123",
            name="Linus",
            age=18,
        )

    async def resolve_all_patients(root, info):
        # import random
        # return [
        #     dict(
        #         id=f"patient{i}",
        #         sex=random.choice([
        #             PatientSexGQL.MALE,
        #             PatientSexGQL.FEMALE,
        #             PatientSexGQL.DIVERSE,
        #         ]),
        #         birthday=random_date(date(1950, 1, 1), date.today()),
        #         concern="",
        #         admission_date=date.today(),
        #         status=PatientStatusGQL.NEW,
        #     )
        #     for i in range(50)
        # ]
        return await patient_pydantic.from_queryset(PatientModel.all())

    async def resolve_get_patient(root, info, id: int):
        patient = await patient_pydantic.from_queryset_single(PatientModel.get(id=id))
        return dict(
            id=id,
            sex=patient.sex,
            birthday=patient.birthday,
            concern=patient.concern,
            admission_date=date.today(),
            status=patient.status
        )


# Example implementation ?

class PatientQuery(graphene.ObjectType):

    patient = graphene.Field(Patient, id=graphene.Int(required=True), required=True)

    # How to get a correct procedure query here?
    procedures = graphene.List(graphene.NonNull(ProceduresModel), required=True)

    async def resolve_get_patient(root, info, id: int):

        patient = await patient_pydantic.from_queryset_single(PatientModel.get(id=id))

        return dict(
            id=id,
            sex=patient.sex,
            birthday=patient.birthday,
            concern=patient.concern,
            admission_date=date.today(),
            status=patient.status,
        )


class ProcedureQuery(graphene.ObjectType):

    procedure = graphene.Field(Procedure, id=graphene.Int(required=True), required=True)

    # How to query patients here? Is "patient_id" which is returned by this resolver then needed in PatientQuery?
    patient = graphene.Field(Patient, id=graphene.Int(required=True), required=True)

    async def resolve_get_procedure(root, info, id: int):

        procedure = await patient_pydantic.from_queryset_single(ProceduresModel.get(id=id))

        return dict(
            id=id,
            date=procedure.date,
            reason=procedure.reason,
            patient_id=procedure.patient,
        )