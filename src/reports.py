"""Pure calculations used to create expense summaries."""

from collections import defaultdict

from src.expense import Expense


def calculate_total(expenses: list[Expense]) -> float:
    """Return the total amount spent across all expenses."""
    return round(sum(expense.amount for expense in expenses), 2)


def total_by_category(expenses: list[Expense]) -> dict[str, float]:
    """Return spending totals grouped by category."""
    category_totals: defaultdict[str, float] = defaultdict(float)
    for expense in expenses:
        category_totals[expense.category] += expense.amount
    return {
        category: round(total, 2)
        for category, total in sorted(
            category_totals.items(), key=lambda item: item[1], reverse=True
        )
    }


def total_by_month(expenses: list[Expense]) -> dict[str, float]:
    """Return spending totals grouped by YYYY-MM from the expense date."""
    month_totals: defaultdict[str, float] = defaultdict(float)
    for expense in expenses:
        month_totals[expense.date[:7]] += expense.amount
    return {
        month: round(total, 2)
        for month, total in sorted(month_totals.items())
    }
