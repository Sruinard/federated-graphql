from dataclasses import dataclass


@dataclass
class Company:
    id: str
    name: str
    ceo: str
    rating: int
    industry: str

