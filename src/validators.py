"""Validation helpers for data entered through the command line."""

from datetime import datetime


def validate_required_text(value: str) -> str:
    """Return stripped text, rejecting a blank value."""
    cleaned_value = value.strip()
    if not cleaned_value:
        raise ValueError("This field cannot be blank.")
    return cleaned_value


def validate_amount(value: str) -> float:
    """Convert a positive amount of money to a float."""
    try:
        amount = float(value)
    except ValueError as error:
        raise ValueError("Enter a number, for example 125.50.") from error

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(amount, 2)


def validate_date(value: str) -> str:
    """Return a date only when it uses the YYYY-MM-DD format."""
    try:
        parsed_date = datetime.strptime(value.strip(), "%Y-%m-%d")
    except ValueError as error:
        raise ValueError("Use a real date in YYYY-MM-DD format.") from error
    return parsed_date.strftime("%Y-%m-%d")


def validate_expense_id(value: str) -> int:
    """Convert a positive whole-number expense ID to an integer."""
    try:
        expense_id = int(value.strip())
    except ValueError as error:
        raise ValueError("Enter a whole-number expense ID.") from error

    if expense_id <= 0:
        raise ValueError("Expense ID must be greater than zero.")
    return expense_id
