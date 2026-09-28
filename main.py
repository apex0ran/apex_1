"""Command-line entry point for the Student Expense Tracker.


"""

from pathlib import Path
from typing import Callable

from src.expense import Expense
from src.expense_manager import ExpenseManager
from src.reports import calculate_total, total_by_category, total_by_month
from src.storage import ExpenseStorage
from src.validators import (
    validate_amount,
    validate_date,
    validate_expense_id,
    validate_required_text,
)


MENU_OPTIONS = {
    "1": "Add an expense",
    "2": "View all expenses",
    "3": "Search or filter expenses",
    "4": "View spending summary",
    "5": "Save expenses",
    "6": "Exit",
    "7": "Edit an expense",
    "8": "Delete an expense",
}


def display_menu() -> None:
    """Print the choices available to the user."""
    print("\n" + "=" * 43)
    print("        STUDENT EXPENSE TRACKER")
    print("=" * 43)
    for option, label in MENU_OPTIONS.items():
        print(f"{option}. {label}")
    print("-" * 43)


def get_menu_choice(input_function: Callable[[str], str] = input) -> str:
    """Return one valid menu choice, asking again after invalid input."""
    while True:
        choice = input_function("Enter your choice (1-8): ").strip()
        if choice in MENU_OPTIONS:
            return choice
        print("Invalid choice. Please enter a number from 1 to 8.")


def show_phase_message(feature_name: str) -> None:
    """Explain that a selected feature belongs to a later build phase."""
    print(f"\n{feature_name} will be implemented in a later phase.")
    print("For now, the menu and input validation are working.")


def get_validated_input(
    prompt: str,
    validator: Callable[[str], object],
    input_function: Callable[[str], str] = input,
) -> object:
    """Keep asking for a value until the supplied validator accepts it."""
    while True:
        try:
            return validator(input_function(prompt))
        except ValueError as error:
            print(f"Invalid input: {error}")


def add_expense(manager: ExpenseManager) -> None:
    """Collect one expense from the user and add it to the manager."""
    print("\nAdd a new expense")
    print("-" * 43)
    amount = get_validated_input("Amount: Rs. ", validate_amount)
    category = get_validated_input("Category: ", validate_required_text)
    date = get_validated_input("Date (YYYY-MM-DD): ", validate_date)
    note = input("Note (optional): ").strip()

    expense = manager.add_expense(amount, category, date, note)
    print(f"Expense #{expense.expense_id} added successfully.")


def get_optional_validated_input(
    prompt: str, validator: Callable[[str], object], current_value: object
) -> object:
    """Return a validated replacement, or keep the current value when blank."""
    while True:
        value = input(prompt)
        if not value.strip():
            return current_value
        try:
            return validator(value)
        except ValueError as error:
            print(f"Invalid input: {error}")


def display_expenses(expenses: list[Expense], heading: str = "Expenses") -> None:
    """Print a readable table of expenses, or explain when none were found."""
    print(f"\n{heading}")
    print("-" * 75)
    if not expenses:
        print("No expenses found.")
        return

    print(f"{'ID':<5}{'Date':<13}{'Category':<18}{'Amount (Rs.)':<15}Note")
    print("-" * 75)
    for expense in expenses:
        print(
            f"{expense.expense_id:<5}{expense.date:<13}{expense.category:<18}"
            f"{expense.amount:<15.2f}{expense.note}"
        )
    print("-" * 75)
    print(f"Total records: {len(expenses)}")


def search_expenses(manager: ExpenseManager) -> None:
    """Let the user filter saved expenses by one criterion."""
    print("\nSearch or filter expenses")
    print("1. Filter by category")
    print("2. Filter by date")
    print("3. Return to main menu")

    filter_choice = input("Enter your choice (1-3): ").strip()
    if filter_choice == "1":
        category = get_validated_input("Category: ", validate_required_text)
        display_expenses(manager.filter_by_category(category), "Category filter results")
    elif filter_choice == "2":
        date = get_validated_input("Date (YYYY-MM-DD): ", validate_date)
        display_expenses(manager.filter_by_date(date), "Date filter results")
    elif filter_choice == "3":
        return
    else:
        print("Invalid choice. Returning to the main menu.")


def display_spending_summary(expenses: list[Expense]) -> None:
    """Print total, category-wise, and monthly spending information."""
    print("\nSpending summary")
    print("-" * 43)
    if not expenses:
        print("No expenses are available for a summary.")
        return

    print(f"Total spent: Rs. {calculate_total(expenses):.2f}")

    print("\nBy category")
    for category, total in total_by_category(expenses).items():
        print(f"- {category}: Rs. {total:.2f}")

    print("\nBy month")
    for month, total in total_by_month(expenses).items():
        print(f"- {month}: Rs. {total:.2f}")


def edit_expense(manager: ExpenseManager) -> None:
    """Update one saved expense while allowing unchanged fields to stay blank."""
    expense_id = get_validated_input("\nExpense ID to edit: ", validate_expense_id)
    expense = manager.get_expense_by_id(expense_id)
    if expense is None:
        print("No expense exists with that ID.")
        return

    display_expenses([expense], "Current expense")
    print("Leave an entry blank to keep its current value.")
    amount = get_optional_validated_input(
        f"New amount (currently Rs. {expense.amount:.2f}): ", validate_amount, expense.amount
    )
    category = get_optional_validated_input(
        f"New category (currently {expense.category}): ",
        validate_required_text,
        expense.category,
    )
    date = get_optional_validated_input(
        f"New date (currently {expense.date}): ", validate_date, expense.date
    )
    new_note = input("New note (blank keeps it; - clears it): ").strip()
    note = "" if new_note == "-" else (new_note or expense.note)

    manager.update_expense(expense_id, amount, category, date, note)
    print(f"Expense #{expense_id} updated. Choose 5 to save the change.")


def delete_expense(manager: ExpenseManager) -> None:
    """Ask for confirmation before removing one saved expense."""
    expense_id = get_validated_input("\nExpense ID to delete: ", validate_expense_id)
    expense = manager.get_expense_by_id(expense_id)
    if expense is None:
        print("No expense exists with that ID.")
        return

    display_expenses([expense], "Expense selected for deletion")
    confirmation = input("Type y to permanently remove this expense: ").strip().lower()
    if confirmation != "y":
        print("Deletion cancelled.")
        return

    manager.delete_expense(expense_id)
    print(f"Expense #{expense_id} deleted. Choose 5 to save the change.")


def main() -> None:
    """Run the menu until the user chooses Exit."""
    data_file = Path(__file__).parent / "data" / "expenses.json"
    storage = ExpenseStorage(data_file)
    manager = ExpenseManager(storage.load())

    print("Welcome! Track your expenses and understand your spending.")
    print(f"Loaded {manager.expense_count} expense(s).")

    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            add_expense(manager)
        elif choice == "2":
            display_expenses(manager.expenses, "All expenses")
        elif choice == "3":
            search_expenses(manager)
        elif choice == "4":
            display_spending_summary(manager.expenses)
        elif choice == "5":
            storage.save(manager.expenses)
            print(f"\nSaved {manager.expense_count} expense(s) to data/expenses.json.")
        elif choice == "6":
            print("\nThank you for using Student Expense Tracker. Goodbye!")
            break
        elif choice == "7":
            edit_expense(manager)
        elif choice == "8":
            delete_expense(manager)


if __name__ == "__main__":
    main()
