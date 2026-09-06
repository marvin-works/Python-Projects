import sqlite3

class Expense:

    def __init__(self, date, description, amount):
        self.date = date
        self.description = description
        self.amount = amount


class ExpenseTracker:

    def __init__(self):
        self.connection = sqlite3.connect("expenses.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL
            )
        """)

        self.connection.commit()

    def add_expense(self, expense):
        self.cursor.execute("""
            INSERT INTO expenses (date, description, amount)
            VALUES (?, ?, ?)
        """, (expense.date, expense.description, expense.amount))

        self.connection.commit()

        print("Expense added successfully.")

    def remove_expense(self, expense_id):
        self.cursor.execute("""
            DELETE FROM expenses
            WHERE id = ?
        """, (expense_id,))

        self.connection.commit()

        if self.cursor.rowcount > 0:
            print("Expense removed successfully.")
        else:
            print("Invalid expense ID.")

    def view_expenses(self):
        self.cursor.execute("""
            SELECT id, date, description, amount
            FROM expenses
        """)

        expenses = self.cursor.fetchall()

        if not expenses:
            print("No expenses found.")
        else:
            print("\nExpense List:")

            for expense in expenses:
                print(
                    f"{expense[0]}. "
                    f"Date: {expense[1]}, "
                    f"Description: {expense[2]}, "
                    f"Amount: ₦{expense[3]:.2f}"
                )

    def total_expenses(self):
        self.cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
        """)

        total = self.cursor.fetchone()[0]

        if total is None:
            total = 0

        print(f"Total Expenses: ₦{total:.2f}")

    def close_database(self):
        self.connection.close()


def main():

    tracker = ExpenseTracker()

    while True:

        print("\nExpenseTracker Menu:")
        print("1. Add Expense")
        print("2. Remove Expense")
        print("3. View Expenses")
        print("4. Total Expenses")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":

            date = input("Enter the date (YYYY-MM-DD): ")
            description = input("Enter the description: ")

            try:
                amount = float(input("Enter the amount: "))

                expense = Expense(
                    date,
                    description,
                    amount
                )

                tracker.add_expense(expense)

            except ValueError:
                print("Please enter a valid number for the amount.")

        elif choice == "2":

            try:
                expense_id = int(
                    input("Enter the expense ID to remove: ")
                )

                tracker.remove_expense(expense_id)

            except ValueError:
                print("Please enter a valid ID.")

        elif choice == "3":

            tracker.view_expenses()

        elif choice == "4":

            tracker.total_expenses()

        elif choice == "5":

            tracker.close_database()

            print("Bye 👋, see you later!")
            break

        else:

            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()