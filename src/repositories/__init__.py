from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import List

from core.customers import Customer
from core.orders import Order
from core.products import Product
from repositories.file_based_repository import FileBasedRepository


@dataclass
class RawOrder:
    id: int
    customer: int
    products: List[int]


class CustomerRepository(FileBasedRepository):
    input_file_path = Path("/etc/data/customers.csv")
    row_transformation_functions = [
        int,
        str,
        str,
    ]
    type_class = Customer


class ProductRepository(FileBasedRepository):
    input_file_path = Path("/etc/data/products.csv")
    row_transformation_functions = [
        int,
        str,
        Decimal,
    ]
    type_class = Product


class OrderRepository(FileBasedRepository):
    input_file_path = Path("/etc/data/orders.csv")
    row_transformation_functions = [
        int,
        int,
        lambda products: [int(product_id) for product_id in products.split(" ")],
    ]
    type_class = RawOrder

    def __init__(self) -> None:
        super().__init__()

        row: RawOrder
        for row in self._rows.values():
            products = [
                ProductRepository().get(product_id) for product_id in row.products
            ]
            product_sum_amount = sum(product.cost for product in products)
            total_amount = Decimal(product_sum_amount).quantize(Decimal("0.01"))
            customer = CustomerRepository().get(row.customer)
            order = Order(
                id=row.id, products=products, customer=customer, euros=total_amount
            )

            self._rows[order.id] = order
