from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Product:
    id: int
    name: str
    cost: Decimal
