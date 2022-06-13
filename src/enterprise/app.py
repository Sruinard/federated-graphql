from typing import List, Optional

import strawberry
from strawberry.asgi import GraphQL
from fastapi import FastAPI
import requests


def get_number_of_products_on_platform():
    query = """query { allProducts { name solutionArea } }"""
    solution_areas = []
    response = requests.post("https://catalogue.wittypebble-179ef70d.westeurope.azurecontainerapps.io/graphql", json={"query": query}).json()["data"]["allProducts"]
    all_solution_areas = set([item["solutionArea"] for item in response])
    for solution_area in all_solution_areas:
        n_products = 0
        for product in response:
            if product["solutionArea"] == solution_area:
                n_products += 1

        solution_areas.append(SolutionArea(
            name=solution_area,
            number_of_products=n_products
        ))

    
    return Platform(
        name="Azure Platform",
        solution_areas = solution_areas
    )

@strawberry.federation.type(description="Provides information about a solution area on Azure")
class SolutionArea:
    name: str
    number_of_products: int

@strawberry.federation.type(description="Azure Product")
class Platform:
    name: str
    solution_areas: List[SolutionArea]


@strawberry.type
class CoreFeature:
    name: str
    status: str

def get_core_features(root: "Product"):
    core_features_data = {
        "a": [("ManagedIdentity", "GA")],
        "b": [("ManagedIdentity", "NotImplemented")],
        "c": [("ManagedIdentity", "GA")],
        "d": [("ManagedIdentity", "GA")],
        "e": [("ManagedIdentity", "GA")],
        "f": [("ManagedIdentity", "GA")],
        "g": [("ManagedIdentity", "GA")],
        "h": [("ManagedIdentity", "GA")],
        "i": [("ManagedIdentity", "NotImplemented")],
    }
    data = core_features_data[root.id]
    return [
        CoreFeature(name=name, status=status)
        for name, status in data
        ]



@strawberry.federation.type(extend=True, keys=["id"])
class Product:
    id: strawberry.ID = strawberry.federation.field(external=True)
    core_features: List[CoreFeature] = strawberry.field(resolver=get_core_features)

    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        return Product(id=id)

@strawberry.type
class Query:
    _service: Optional[str]
    platform: Platform = strawberry.field(resolver=get_number_of_products_on_platform, description="Get information on the Azure Platform") 

###########################################################################
###########################################################################
###########################################################################

schema = strawberry.federation.Schema(query=Query, types=[Product])

graphql_app = GraphQL(schema)
app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)