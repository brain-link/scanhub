import graphene
from datetime import date
from tortoise.contrib.pydantic import pydantic_model_creator
from scanhub.graphene.random_date import random_date
from scanhub.graphene.types import Patient, PatientSexGQL, PatientStatusGQL, User
from scanhub.database.models import Patient as dbPatient

patient_pydantic = pydantic_model_creator(dbPatient)

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
        return await patient_pydantic.from_queryset(dbPatient.all())

    async def resolve_get_patient(root, info, id: int):
        patient = await patient_pydantic.from_queryset_single(dbPatient.get(id=id))
        print(patient.concern)
        return dict(
            id=id,
            sex=patient.sex,
            birthday=patient.birthday,
            concern=patient.concern,
            admission_date=date.today(),
            status=patient.status
        )
