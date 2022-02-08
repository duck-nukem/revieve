import unittest

from core.customers import Customer
from core.products import Product
from repositories import OrderRepository


class TestOrderRepository(unittest.TestCase):
    def test_denormalization(self):
        repository = OrderRepository()

        results = repository.list()

        self.assertIsInstance(results[0].customer, Customer)
        self.assertIsInstance(results[0].products[0], Product)


if __name__ == "__main__":
    unittest.main()
