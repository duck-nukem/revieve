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
    orders_sorted_by_customer_id = sorted(
        OrderRepository().list(), key=lambda o: o.customer.id
    )
    sum_of_spent_amount_by_customer = [
        [
            str(customer.id),
            customer.firstname,
            customer.lastname,
            sum(map(lambda o: o.euros, orders)),
        ]
        for customer, orders in groupby(
            orders_sorted_by_customer_id,
            key=lambda o: o.customer,
        )
    ]

    CsvReport("customer_ranking").write(
        headers=["id", "firstname", "lastname", "total_euros"],
        rows=sorted(
            sum_of_spent_amount_by_customer, key=lambda row: row[3], reverse=True
        ),
    )


def generate_product_customers():
    customers_by_product_id = defaultdict(set)

    order: Order
    for order in OrderRepository().list():
        for product in order.products:
            customers_by_product_id[product.id].add(str(order.customer.id))

    CsvReport("product_customers").write(
        headers=["id", "customer_ids"],
        rows=[
            [str(key), " ".join(value)]
            for key, value in customers_by_product_id.items()
        ],
    )
