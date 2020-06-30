from pydantic.dataclasses import dataclass

@dataclass
class HouseholdProduct:
    name: str
    price: float
