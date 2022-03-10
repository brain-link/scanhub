import graphene
from datetime import date
from scanhub.graphene.random_date import random_date

from scanhub.graphene.types import Patient, PatientSexGQL, PatientStatusGQL, User


class Query(graphene.ObjectType):
    me = graphene.Field(User)
    all_patients = graphene.List(graphene.NonNull(Patient), required=True)

    def resolve_me(root, info):
        return dict(
            id="username123",
            name="Linus",
            age=18,
        )

    def resolve_all_patients(root, info):
        import random
        return [
            dict(
                id=f"patient{i}",
                sex=random.choice([
                    PatientSexGQL.MALE,
                    PatientSexGQL.FEMALE,
                    PatientSexGQL.DIVERSE,
                ]),
                birthday=random_date(date(1950, 1, 1), date.today()),
                concern="",
                admission_date=date.today(),
                status=PatientStatusGQL.NEW,
            )
            for i in range(50)
        ]
