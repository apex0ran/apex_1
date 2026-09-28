

import tempfile
import unittest
from pathlib import Path

from src.expense_manager import ExpenseManager
from src.reports import calculate_total, total_by_category, total_by_month
from src.storage import ExpenseStorage


class ExpenseManagerTests(unittest.TestCase):
    """Check adding an expense and saving it to JSON."""

    def test_new_expenses_receive_incrementing_ids(self) -> None:
        manager = ExpenseManager()

        first = manager.add_expense(50.0, "Food", "2026-09-26")
        second = manager.add_expense(25.0, "Travel", "2026-09-27")

        self.assertEqual(first.expense_id, 1)
        self.assertEqual(second.expense_id, 2)

    def test_saved_expenses_can_be_loaded_again(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            storage = ExpenseStorage(Path(temporary_directory) / "expenses.json")
            manager = ExpenseManager()
            manager.add_expense(120.5, "Books", "2026-09-26", "Python guide")

            storage.save(manager.expenses)
            loaded_expenses = storage.load()

        self.assertEqual(len(loaded_expenses), 1)
        self.assertEqual(loaded_expenses[0].category, "Books")
        self.assertEqual(loaded_expenses[0].note, "Python guide")

    def test_category_filter_is_case_insensitive(self) -> None:
        manager = ExpenseManager()
        manager.add_expense(50.0, "Food", "2026-09-26")
        manager.add_expense(20.0, "Travel", "2026-09-26")

        results = manager.filter_by_category("food")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].amount, 50.0)

    def test_date_filter_returns_only_matching_expenses(self) -> None:
        manager = ExpenseManager()
        manager.add_expense(50.0, "Food", "2026-09-26")
        manager.add_expense(20.0, "Travel", "2026-09-27")

        results = manager.filter_by_date("2026-09-27")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].category, "Travel")

    def test_reports_calculate_totals_by_category_and_month(self) -> None:
        manager = ExpenseManager()
        manager.add_expense(50.0, "Food", "2026-09-26")
        manager.add_expense(25.0, "Food", "2026-10-01")
        manager.add_expense(20.0, "Travel", "2026-10-02")

        self.assertEqual(calculate_total(manager.expenses), 95.0)
        self.assertEqual(total_by_category(manager.expenses), {"Food": 75.0, "Travel": 20.0})
        self.assertEqual(total_by_month(manager.expenses), {"2026-09": 50.0, "2026-10": 45.0})

    def test_existing_expense_can_be_updated(self) -> None:
        manager = ExpenseManager()
        expense = manager.add_expense(50.0, "Food", "2026-09-26", "Lunch")

        was_updated = manager.update_expense(
            expense.expense_id, 75.0, "Books", "2026-09-27", "Textbook"
        )

        self.assertTrue(was_updated)
        self.assertEqual(expense.amount, 75.0)
        self.assertEqual(expense.category, "Books")
        self.assertEqual(expense.note, "Textbook")

    def test_existing_expense_can_be_deleted(self) -> None:
        manager = ExpenseManager()
        expense = manager.add_expense(50.0, "Food", "2026-09-26")

        was_deleted = manager.delete_expense(expense.expense_id)

        self.assertTrue(was_deleted)
        self.assertEqual(manager.expense_count, 0)
        self.assertFalse(manager.delete_expense(expense.expense_id))
