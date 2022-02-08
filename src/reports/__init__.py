from collections import defaultdict
from itertools import groupby

from core.orders import Order
from reports.csv_report import CsvReport
from repositories import OrderRepository


def generate_order_prices():
    CsvReport("order_prices").write(
        headers=["id", "euros"],
        rows=map(lambda row: [row.id, row.euros], OrderRepository().list()),
    )


def generate_customer_ranking():
    CsvReport("customer_ranking").write(
        headers=["id", "firstname", "lastname", "total_euros"],
        rows=[
            [
                str(customer.id),
                customer.firstname,
                customer.lastname,
                sum(map(lambda o: o.euros, orders)),
            ]
            for customer, orders in groupby(
                OrderRepository().list(), key=lambda o: o.customer
            )
        ],
    )


def generate_product_customers():
    customers_by_product_id = defaultdict(list)

    order: Order
    for order in OrderRepository().list():
        for product in order.products:
            customers_by_product_id[product.id].append(str(order.customer.id))

    CsvReport("product_customers").write(
        headers=["id", "customer_ids"],
        rows=[
            [str(key), " ".join(value)]
            for key, value in customers_by_product_id.items()
        ],
    )
