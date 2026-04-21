from datetime import datetime

class ExpenseTracker:
    def __init__(self):
        """Initialize expense tracker"""
        self.expenses = []
        self.income = 0
        self.categories = [
            "Food", "Transport",
            "Housing", "Entertainment",
            "Healthcare", "Education",
            "Shopping", "Bills", "Other"
        ]

    def add_expense(self, category,
                   amount, description=""):
        """Add new expense"""
        if category not in self.categories:
            category = "Other"

        expense = {
            "id": len(self.expenses) + 1,
            "category": category,
            "amount": float(amount),
            "description": description,
            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )
        }

        self.expenses.append(expense)
        return {
            "status": "success",
            "message": f"Added {category}: ${amount}",
            "expense": expense
        }

    def get_summary(self):
        """Get expense summary"""
        if not self.expenses:
            return {
                "status": "empty",
                "message": "No expenses yet"
            }

        # Calculate totals by category
        category_totals = {}
        for exp in self.expenses:
            cat = exp["category"]
            if cat not in category_totals:
                category_totals[cat] = 0
            category_totals[cat] += exp["amount"]

        total = sum(
            exp["amount"] for exp in self.expenses
        )

        return {
            "status": "success",
            "total_expenses": round(total, 2),
            "income": self.income,
            "savings": round(self.income - total, 2),
            "category_breakdown": category_totals,
            "expense_count": len(self.expenses),
            "expenses": self.expenses
        }

    def set_income(self, amount):
        """Set monthly income"""
        self.income = float(amount)
        return {
            "status": "success",
            "message": f"Income set to ${amount}"
        }

    def delete_expense(self, expense_id):
        """Delete expense by ID"""
        self.expenses = [
            exp for exp in self.expenses
            if exp["id"] != expense_id
        ]
        return {
            "status": "success",
            "message": "Expense deleted"
        }

    def get_by_category(self, category):
        """Get expenses by category"""
        filtered = [
            exp for exp in self.expenses
            if exp["category"] == category
        ]
        return {
            "status": "success",
            "category": category,
            "expenses": filtered,
            "total": sum(
                exp["amount"] for exp in filtered
            )
        }
