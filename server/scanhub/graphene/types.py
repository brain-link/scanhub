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
