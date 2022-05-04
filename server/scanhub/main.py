from cgitb import reset
import graphene
import uvicorn
import json
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from tortoise.contrib.fastapi import register_tortoise

from scanhub.graphene.query import Query
from scanhub.graphene.subscription import Subscription
from scanhub.graphene.mutation import Mutation


app = FastAPI(
    title="ScanHub"
)

schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)

# Graphiql IDE
app.mount("/graphql", GraphQLApp(schema, on_get=make_graphiql_handler()))

# Tortoise ORM    
register_tortoise(
    app,
    db_url='postgres://brainLink:brainLinkIstCool2022UndLecker@postgres/scanhub',
    modules={"models": ["scanhub.database.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
