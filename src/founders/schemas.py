import strawberry


@strawberry.federation.type(keys=["id"], description="Azure Product")
class Founder:
    id: strawberry.ID
    name: str
