import graphene
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from scanhub.graphene.query import Query
from scanhub.graphene.subscription import Subscription
from scanhub.graphene.mutation import Mutation



from tortoise import Tortoise



async def connectToDatabase():
    await Tortoise.init(
        db_url='postgres://brainLink:brainLinkIstCool2022UndLecker@postgres/scanhub',
        modules={"models": ["scanhub.database.models"]}
    )

    # register_tortoise(
    #     admin_app,
    #     config={
    #         "connections": {"default": settings.DATABASE_URL},
    #         "apps": {
    #             "models": {
    #                 "models": ["scanhub.models"],
    #                 "default_connection": "default",
    #             }
    #         },
    #     },
    #     generate_schemas=True,
    # )

    # register_tortoise(
    #     admin_app,
    #     db_url="postgres://brainLink:brainLinkIstCool2022UndLecker@postgres/scanhub",
    #     modules={"models": ["scanhub.models"]},
    #     generate_schemas=True,
    #     add_exception_handlers=True,
    # )



app = FastAPI()
schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)

# Graphiql IDE
app.mount("/", GraphQLApp(schema, on_get=make_graphiql_handler()))

connectToDatabase()
Tortoise.generate_schemas()
# await connectToDatabase()
# await Tortoise.generate_schemas()