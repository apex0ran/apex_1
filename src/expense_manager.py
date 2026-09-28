

from src.expense import Expense


class ExpenseManager:
    """Store expense objects and assign each new one a unique ID."""

    def __init__(self, expenses: list[Expense] | None = None) -> None:
        self.expenses = expenses or []

    @property
    def expense_count(self) -> int:
        """Return how many expenses are currently stored in memory."""
        return len(self.expenses)

    def add_expense(self, amount: float, category: str, date: str, note: str = "") -> Expense:
        """Create, store, and return a new expense."""
        next_id = max((expense.expense_id for expense in self.expenses), default=0) + 1
        expense = Expense(next_id, amount, category, date, note)
        self.expenses.append(expense)
        return expense

    def filter_by_category(self, category: str) -> list[Expense]:
        """Return expenses whose category matches without case sensitivity."""
        requested_category = category.strip().lower()
        return [
            expense
            for expense in self.expenses
            if expense.category.lower() == requested_category
        ]

    def filter_by_date(self, date: str) -> list[Expense]:
        """Return expenses recorded on one exact date."""
        return [expense for expense in self.expenses if expense.date == date]

    def get_expense_by_id(self, expense_id: int) -> Expense | None:
        """Return one expense by ID, or None when it does not exist."""
        for expense in self.expenses:
            if expense.expense_id == expense_id:
                return expense
        return None

    def update_expense(
        self, expense_id: int, amount: float, category: str, date: str, note: str
    ) -> bool:
        """Replace an existing expense's editable fields."""
        expense = self.get_expense_by_id(expense_id)
        if expense is None:
            return False

        expense.amount = amount
        expense.category = category
        expense.date = date
        expense.note = note
        return True

    def delete_expense(self, expense_id: int) -> bool:
        """Remove an expense by ID and report whether it was found."""
        expense = self.get_expense_by_id(expense_id)
        if expense is None:
            return False

        self.expenses.remove(expense)
        return True
