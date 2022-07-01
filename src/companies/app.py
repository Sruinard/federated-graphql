from typing import List, Optional

import requests
import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL

import repo
import schemas

###################################################
###################################################
###################################################


@strawberry.type(description="Payment provides information about the amount transferred to the recipient")
class Payment:
    id: strawberry.ID
    amount: str
    recipient: str

###################################################
###################################################
###################################################


def get_orders(root: "Account"):
    core_features_data = {
        "a": [("a1", "$150", "IBANXXXXXXXXX"), ("a2", "$80", "IBANXXXXXXXXX")],
        "b": [("b1", "$1150", "IBANXXXXXXXXX"), ("b2", "$20", "IBANXXXXXXXXX"), ("b3", "$2220", "IBANXXXXXXXXX")],
    }
    data = core_features_data[root.id]
    return [
        Payment(id=id, amount=amount, recipient=recipient)
        for id, amount, recipient in data
    ]


###################################################
###################################################
###################################################

@strawberry.federation.type(extend=True, keys=["id"])
class Account:
    id: strawberry.ID = strawberry.federation.field(external=True)
    orders: List[Payment] = strawberry.field(resolver=get_orders)

    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        return Account(id=id)


###################################################
###################################################
###################################################


@strawberry.type
class Query:
    _service: Optional[str]
    companies: List[schemas.Company] = strawberry.field(
        resolver=repo.CompanyRepoInstance.get, description="Retrieves all accounts registered on our service")

@strawberry.type
class Mutation:
    @strawberry.mutation(description="Creates a new account")
    def add_company(self, name: str, ceo: str, rating: int, number_of_employees: int) -> schemas.Company:
        company = repo.CompanyRepoInstance.add_company(name, ceo, rating, number_of_employees)
        return company

schema = strawberry.federation.Schema(query=Query, mutation=Mutation, types=[schemas.Founder])

graphql_app = GraphQL(schema)
app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
