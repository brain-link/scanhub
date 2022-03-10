import graphene
from graphene_file_upload.scalars import Upload


class FileUploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        return FileUploadMutation(ok=True)


class Mutation(graphene.ObjectType):
    upload_file = FileUploadMutation.Field()
