import csv
from functools import reduce
from pathlib import Path
from typing import Any, Callable, List

from src.input_transformers.exceptions import (
    InvalidInputFileException,
    InvalidRowConfigurationException,
)


def _deserialize_column(value: Any, transformer: Callable, header: str) -> Any:
    return {header: transformer(value)}


def transform(file_path: Path, row_config: List = None) -> List:
    with open(file_path) as csvfile:
        reader_rows = csv.reader(csvfile)
        headers = next(reader_rows, None)
        is_file_empty = headers is None

        if is_file_empty:
            raise InvalidInputFileException("File is empty")

        if len(headers) != len(row_config):
            raise InvalidRowConfigurationException(
                "The supplied transformation functions aren't equal to the number of columns in the input file"
            )

        transformed_data = [
            reduce(
                lambda row_dict, column: row_dict | _deserialize_column(*column),
                zip(row, row_config, headers),
                dict(),
            )
            for row in reader_rows
        ]

        return transformed_data
