import unittest
from decimal import Decimal
from pathlib import Path
from unittest import TestCase

from src.input_transformers.csv import transform
from src.input_transformers.exceptions import (
    InvalidInputFileException,
    InvalidRowConfigurationException,
)

_PATH = Path(__file__).resolve().parent


class TestCsvInputTransformer(TestCase):
    def test_empty_file_raises_exception(self):
        with self.assertRaises(InvalidInputFileException):
            transform(_PATH / "samples/empty.csv")

    def test_mismatching_configuration_and_columns_raises_exception(self):
        with self.assertRaises(InvalidRowConfigurationException):
            transform(_PATH / "samples/valid.csv", row_config=[str, str])

    def test_parses_valid_csv(self):
        row_config = [
            lambda row_id: int(row_id) + 1,
            str,
            lambda cost: Decimal(cost).quantize(Decimal("0.01")),
        ]

        parsed_rows = transform(_PATH / "samples/valid.csv", row_config=row_config)

        self.assertEqual(
            parsed_rows,
            [
                {
                    "id": 1,
                    "name": "screwdriver",
                    "cost": Decimal("2.98"),
                },
                {
                    "id": 2,
                    "name": "hammer",
                    "cost": Decimal("4.32"),
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
