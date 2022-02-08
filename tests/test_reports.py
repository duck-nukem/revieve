import unittest
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch

from core.customers import Customer
from core.orders import Order
from core.products import Product
from reports import (
    generate_order_prices,
    generate_product_customers,
    generate_customer_ranking,
)


@patch("reports.CsvReport")
@patch("reports.OrderRepository")
class TestReports(TestCase):
    def test_order_prices(self, patched_order_repository, patched_report):
        sample_order = Order(
            id=1,
            customer=Customer(id=1, firstname="", lastname=""),
            products=[],
            euros=Decimal("0.00"),
        )
        patched_order_repository.return_value.list.return_value = [sample_order]

        generate_order_prices()

        self.assertEqual(
            ["id", "euros"],
            patched_report.return_value.write.mock_calls[0].kwargs["headers"],
        )
        self.assertListEqual(
            list(patched_report.return_value.write.mock_calls[0].kwargs["rows"]),
            [[sample_order.id, sample_order.euros]],
        )

    def test_product_customers(self, patched_order_repository, patched_report):
        hammer = Product(id=1, name="Hammer", cost=Decimal("13.37"))
        alice_hammer_purchase = Order(
            id=1,
            customer=Customer(id=1, firstname="Alice", lastname=""),
            products=[hammer],
            euros=hammer.cost,
        )
        bob_hammer_purchase = Order(
            id=2,
            customer=Customer(id=2, firstname="Bob", lastname=""),
            products=[hammer],
            euros=hammer.cost,
        )
        hammer_orders = [
            alice_hammer_purchase,
            bob_hammer_purchase,
            alice_hammer_purchase,
        ]
        patched_order_repository.return_value.list.return_value = hammer_orders

        generate_product_customers()

        self.assertEqual(
            ["id", "customer_ids"],
            patched_report.return_value.write.mock_calls[0].kwargs["headers"],
        )
        self.assertEqual(
            patched_report.return_value.write.mock_calls[0].kwargs["rows"][0][0],
            str(hammer.id),
        )
        self.assertCountEqual(
            patched_report.return_value.write.mock_calls[0]
            .kwargs["rows"][0][1]
            .split(" "),
            [
                str(alice_hammer_purchase.customer.id),
                str(bob_hammer_purchase.customer.id),
            ],
        )

    def test_customer_ranking(self, patched_order_repository, patched_report):
        product = Product(id=1, name="Hammer", cost=Decimal("13.37"))
        customer = Customer(id=1, firstname="Alice", lastname="")
        bob = Customer(id=2, firstname="Bob", lastname="")
        first_order = Order(
            id=1,
            customer=customer,
            products=[product],
            euros=product.cost,
        )
        second_order = Order(
            id=2,
            customer=customer,
            products=[product],
            euros=product.cost,
        )
        bobs_order = Order(
            id=3,
            customer=bob,
            products=[product, product, product],
            euros=product.cost * 3,
        )
        orders = [
            first_order,
            bobs_order,
            second_order,
        ]
        patched_order_repository.return_value.list.return_value = orders

        generate_customer_ranking()

        self.assertEqual(
            ["id", "firstname", "lastname", "total_euros"],
            patched_report.return_value.write.mock_calls[0].kwargs["headers"],
        )
        self.assertListEqual(
            list(patched_report.return_value.write.mock_calls[0].kwargs["rows"]),
            [
                [
                    str(bob.id),
                    bob.firstname,
                    bob.lastname,
                    bobs_order.euros,
                ],
                [
                    str(customer.id),
                    customer.firstname,
                    customer.lastname,
                    product.cost * 2,
                ],
            ],
        )


if __name__ == "__main__":
    unittest.main()
