from dataclasses import dataclass
from decimal import Decimal
from typing import List

from core.customers import Customer
from core.products import Product


@dataclass
class Order:
    id: int
    customer: Customer
    products: List[Product]
    euros: Decimal
