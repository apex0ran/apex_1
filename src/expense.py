"""Data model for one student expense."""

from dataclasses import dataclass


@dataclass
class Expense:
    """Represent one recorded expense."""

    expense_id: int
    amount: float
    category: str
    date: str
    note: str = ""

    def to_dict(self) -> dict:
        """Convert the expense to a JSON-compatible dictionary."""
        return {
            "expense_id": self.expense_id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Create an Expense object from data loaded from JSON."""
        return cls(
            expense_id=int(data["expense_id"]),
            amount=float(data["amount"]),
            category=str(data["category"]),
            date=str(data["date"]),
            note=str(data.get("note", "")),
        )
