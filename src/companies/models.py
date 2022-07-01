from dataclasses import dataclass


@dataclass
class Company:
    id: str
    name: str
    ceo: str
    rating: int
    number_of_employees: int

