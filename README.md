# Student Expense Tracker

This is a simple command-line Python project. It helps a student keep a record of daily expenses like food, travel, books, and other personal costs.

## What this project can do

- Add a new expense.
- View all saved expenses.
- Search expenses by category or date.
- Show total spending in categories.
- Edit an expense using its ID.
- Delete an expense using its ID.
- Save expenses in a JSON file.

## Tools used

- Python 3
- JSON file storage
- Python `unittest` module for testing

No extra Packages Required to run the program.

## Folder structure

```text
student_expense_tracker/
|-- main.py
|-- README.md
|-- statement.md
|-- requirements.txt
|-- data/
|-- src/
|   |-- expense.py
|   |-- expense_manager.py
|   |-- reports.py
|   |-- storage.py
|   `-- validators.py
`-- tests/
```

## How to run the project

1. Install Python
2. Open terminal in the `student_expense_tracker` folder.
3. Run this command:

   
   `python main.py`
   

4. Choose an option from the menu.

## Menu options

| 1. Add an expense 
| 2. View all expenses 
| 3. Search by category or date 
| 4. View spending summary 
| 5. Save expenses 
| 6. Exit the program 
| 7. Edit an expense 
| 8. Delete an expense 

When adding an expense, enter a amount, a category, and a date in `YYYY-MM-DD` format. The note is optional.

The program saves data in `data/expenses.json`. Choose option 5 after adding, editing, or deleting an expense.

## How to test

Run this command in the project folder:

`
python -m unittest discover -s tests
`

You can also test the program manually by entering a wrong menu option, a negative amount, or an invalid date. The program should show an error message and ask again.

## Python concepts used

- Functions
- Classes and objects
- Lists and dictionaries
- Loops and conditions
- File handling with JSON
- Input validation
- Unit testing
