from typing import List
import os

import strawberry
from strawberry.asgi import GraphQL
from fastapi import FastAPI
import uuid

def get_id():
    return str(uuid.uuid4())


def get_accounts():
    return ACCOUNTS

def get_config():
    return os.environ.get("PORT_NUMBER", "Default configuration showing")

###################################################
###################################################
###################################################

@strawberry.federation.type(keys=["id"], description="Azure Product")
class Account:
    id: strawberry.ID
    name: str

###################################################
###################################################
###################################################


@strawberry.type
class Query:
    all_users: List[Account] = strawberry.field(resolver=get_accounts, description="Retrieves all accounts registered on our service") 
    config: str = strawberry.field(resolver=get_config, description="Retrieves the configuration of our service")

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(self, name) -> Account:
        account = Account(id=get_id(), name=name)
        ACCOUNTS.append(account)
        return account


ACCOUNTS = [
    Account(id=get_id(), name="Stef Ruinard"),
    Account(id=get_id(), name="Jochen van Wylick")
]

schema = strawberry.federation.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
