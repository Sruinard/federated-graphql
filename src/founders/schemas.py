import strawberry


@strawberry.federation.type(keys=["id"], description="Founder entity")
class Founder:
    id: strawberry.ID
    name: str
