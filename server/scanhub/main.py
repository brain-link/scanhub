import graphene
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from scanhub.graphene.query import Query
from scanhub.graphene.subscription import Subscription
from scanhub.graphene.mutation import Mutation

app = FastAPI()
schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)

# Graphiql IDE
app.mount("/", GraphQLApp(schema, on_get=make_graphiql_handler()))
