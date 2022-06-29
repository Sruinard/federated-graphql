from typing import List
import os

import strawberry
from strawberry.asgi import GraphQL
from fastapi import FastAPI

ACCOUNTS = [
            ("a", "Stef Ruinard"),
            ("b", "Jochen van Wylick"),
]

def get_accounts():
    return [
        Account(
            id=id,
            name=name
        )
        for id, name in ACCOUNTS
    ]

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


schema = strawberry.federation.Schema(query=Query)

graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
