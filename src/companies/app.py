from typing import List, Optional

import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL

import repo
import schemas

@strawberry.type
class Query:
    _service: Optional[str]
    companies: List[schemas.Company] = strawberry.field(
        resolver=repo.CompanyRepoInstance.get, description="Retrieves all registered companies")

@strawberry.type
class Mutation:
    @strawberry.mutation(description="Creates a new company")
    def add_company(self, name: str, ceo: str, rating: int, industry: str) -> schemas.Company:
        company = repo.CompanyRepoInstance.add_company(name, ceo, rating, industry)
        return company

schema = strawberry.federation.Schema(query=Query, mutation=Mutation, types=[schemas.Founder])

graphql_app = GraphQL(schema)
app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
