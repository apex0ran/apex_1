"""Read and write expense data in a local JSON file."""

import json
from pathlib import Path

from src.expense import Expense


class ExpenseStorage:
    """Persist expenses without requiring an external database."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load(self) -> list[Expense]:
        """Load saved expenses, or return an empty list for a new project."""
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                saved_data = json.load(file)
            return [Expense.from_dict(item) for item in saved_data]
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            raise ValueError(
                f"Could not read saved expenses from {self.file_path.name}."
            ) from error

    def save(self, expenses: list[Expense]) -> None:
        """Save every expense as formatted JSON."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        data = [expense.to_dict() for expense in expenses]
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
