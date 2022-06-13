from typing import List

import strawberry
from strawberry.asgi import GraphQL
from fastapi import FastAPI

PRODUCTS = [
            ("a", "Azure Container Apps", "containers"),
            ("b", "Azure Kubernetes Service", "containers"),
            ("c", "Azure Functions", "containers"),
            ("d", "Azure Container Instances", "containers"),
            ("e", "Azure Cache for Redis", "databases"),
            ("f", "Azure Cosmos DB", "databases"),
            ("g", "Azure SQL Database", "databases"),
            ("h", "API Management", "integration"),
            ("i", "Logic Apps", "integration"),
]

def get_products():
    return [
        Product(
            id=product_id,
            name=name,
            solution_area=solution_area
        )
        for product_id, name, solution_area in PRODUCTS
    ]

@strawberry.federation.type(keys=["id"], description="Azure Product")
class Product:
    id: strawberry.ID
    name: str
    solution_area: str
    

@strawberry.type
class Query:
    all_products: List[Product] = strawberry.field(resolver=get_products, description="Retrieves all products on the Azure Platform") 


schema = strawberry.federation.Schema(query=Query)



graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
