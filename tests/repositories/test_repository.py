import unittest
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from unittest import TestCase

from src.core.repository.exceptions import (
    UnsupportedDataSourceException,
    ItemNotFoundException,
)
from src.repositories.file_based_repository import FileBasedRepository

_PATH = Path(__file__).resolve().parent


class InvalidToolRepository(FileBasedRepository):
    input_file_path = _PATH / "samples/data_without_id_column.csv"
    row_transformation_functions = [
        lambda row_id: int(row_id) + 1,
        str,
        lambda cost: Decimal(cost).quantize(Decimal("0.01")),
    ]


@dataclass
class Tool:
    id: int
    name: str
    cost: Decimal


class ToolRepository(FileBasedRepository):
    input_file_path = _PATH / "samples/tools.csv"
    type_class = Tool
    row_transformation_functions = [
        lambda row_id: int(row_id) + 1,
        str,
        lambda cost: Decimal(cost).quantize(Decimal("0.01")),
    ]


class TestFileBasedRepository(TestCase):
    def test_raises_exception_if_dataset_doesnt_have_an_id_column(self):
        with self.assertRaises(UnsupportedDataSourceException):
            InvalidToolRepository()

    def test_list(self):
        repository = ToolRepository()

        repository_list = repository.list()

        self.assertEqual(len(repository_list), 2)

    def test_get_by_id(self):
        repository = ToolRepository()

        tool = repository.get(1)

        self.assertEqual(tool.id, 1)

    def test_filter_by_single_value_for_key(self):
        repository = ToolRepository()

        results = repository.filter(id=2)

        self.assertEqual(results[0].id, 2)

    def test_filter_multiple_values_for_key(self):
        repository = ToolRepository()
        missing_item_id = 3

        results = repository.filter(id=[2, missing_item_id])

        self.assertEqual(len(results), 1)

    def test_get_by_id_with_missing_item(self):
        repository = ToolRepository()

        with self.assertRaises(ItemNotFoundException):
            repository.get(-999)


if __name__ == "__main__":
    unittest.main()
