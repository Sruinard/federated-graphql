import strawberry
from typing import List
import repo


@strawberry.type(description="Payment provides information about the amount transferred to the recipient")
class Company:
    id: strawberry.ID
    name: str
    ceo: str
    rating: int
    number_of_empolyees: int



@strawberry.federation.field(requires=["name"])
def get_companies(root: "Founder") -> List[Company]:
    return [Company(id=company.id, name=company.name, ceo=company.ceo) for company in repo.CompanyRepoInstance.get_by_ceo(root.name)]

@strawberry.federation.type(extend=True, keys=["id"])
class Founder:
    id: strawberry.ID = strawberry.federation.field(external=True)
    name: str = strawberry.federation.field(external=True)
    
    @strawberry.federation.field(requires=["name"])
    def companies(root: "Founder") -> List[Company]:
        return [Company(id=company.id, name=company.name, ceo=company.ceo, rating=company.rating, number_of_employees=company.number_of_employees) for company in repo.CompanyRepoInstance.get_by_ceo(root.name)]

    @classmethod
    def resolve_reference(cls, id: strawberry.ID, name: str):
        return Founder(id=id, name=name)
