import csv
from pathlib import Path
from typing import Iterable, Any

REPORT_PATH = Path("/etc/output")


class CsvReport:
    def __init__(self, name):
        self.filename = Path(REPORT_PATH / f"{name}.csv")

    def write(self, headers: Iterable[str], rows: Iterable[Any]) -> None:
        with open(self.filename, "w") as file:
            writer = csv.writer(file)
            writer.writerow(headers)

            for row in rows:
                writer.writerow(row)
