import asyncio
from datetime import date

import graphene
from scanhub.graphene.random_date import random_date

from scanhub.graphene.types import Patient, PatientSexGQL, PatientStatusGQL


class Subscription(graphene.ObjectType):
    data = graphene.List(
        graphene.NonNull(Patient),
        upto=graphene.Int(required=True),
    )

    async def subscribe_data(root, info, upto: int):
        import random
        for i in range(upto):
            yield [
                dict(
                    id=f"patient{random.randrange(50)}",
                    sex=random.choice([PatientSexGQL.FEMALE, PatientSexGQL.MALE, PatientSexGQL.DIVERSE]),
                    birthday=random_date(date(1950, 1, 1), date.today()),
                    concern="",
                    admission_date=date.today(),
                    status=PatientStatusGQL.NEW,
                )
                for i in range(5)
            ]
            await asyncio.sleep(0.05)
