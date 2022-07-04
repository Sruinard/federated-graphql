import os
import uuid
from typing import List, Optional

import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL

import repo
import schemas

FounderRepoInstance = repo.FounderRepo()


def get_config():
    return os.environ.get("PORT_NUMBER", "Default configuration showing")


@strawberry.type
class Query:
    @strawberry.field
    def founders(self, where_name_is: Optional[str] = None) -> List[schemas.Founder]:
        if where_name_is is not None:
            return [FounderRepoInstance.get_by_name(name=where_name_is)]
        return FounderRepoInstance.get()
    config: str = strawberry.field(
        resolver=get_config, description="Retrieves the configuration of our service")


@strawberry.type
class Mutation:
    @strawberry.mutation(description="Creates a new account")
    def add_founder(self, name: str) -> schemas.Founder:
        founder = FounderRepoInstance.add_founder(name)
        return founder


schema = strawberry.federation.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
