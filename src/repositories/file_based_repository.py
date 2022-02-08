from pathlib import Path
from typing import TypeVar, List, Callable

from src.core.repository.base import Repository
from src.core.repository.exceptions import (
    UnsupportedDataSourceException,
    ItemNotFoundException,
)
from src.input_transformers.csv import transform

T = TypeVar("T")


class FileBasedRepository(Repository):
    input_file_path: Path
    row_transformation_functions: List[Callable]
    type_class: T

    def __init__(self) -> None:
        super().__init__()
        input_rows = transform(self.input_file_path, self.row_transformation_functions)

        if "id" not in input_rows[0]:
            raise UnsupportedDataSourceException(
                f"Unsupported data source: {self.input_file_path}. Reason: Missing 'id' column."
            )

        self._rows = {row["id"]: self.type_class(**row) for row in input_rows}

    def get(self, id: int) -> T:
        if id not in self._rows.keys():
            raise ItemNotFoundException(f"Item with id {id} not found.")

        return self._rows[id]

    def list(self) -> List[T]:
        return list(self._rows.values())

    def filter(self, **kwargs) -> List[T]:
        filters = self._build_filters(kwargs)
        results = [
            row
            for row in self._rows.values()
            if any(getattr(row, key) == value for key, value in filters)
        ]

        return results

    @staticmethod
    def _build_filters(kwargs):
        filters = []

        for key, criteria in kwargs.items():
            if isinstance(criteria, list):
                for criterion in criteria:
                    filters.append((key, criterion))
            else:
                filters.append((key, criteria))

        return filters
