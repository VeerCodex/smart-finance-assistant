from flask import (Flask, request,
                   jsonify, render_template)
from src.finance_assistant import FinanceAssistant
from src.google_services import GoogleServices
from src.expense_tracker import ExpenseTracker
from src.utils import (format_currency,
                       calculate_savings_rate,
                       get_financial_health,
                       validate_amount)
import os

app = Flask(__name__)

# Initialize services
assistant = FinanceAssistant()
google_services = GoogleServices()
tracker = ExpenseTracker()

# ==================
# MAIN ROUTES
# ==================

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "vertical": "Finance Assistant",
        "version": "1.0.0"
    })

# ==================
# CHAT ROUTES
# ==================

@app.route('/api/chat', methods=['POST'])
def chat():
    """AI Financial Chat"""
    data = request.get_json()
    message = data.get('message', '').strip()

    if not message:
        return jsonify({
            "status": "error",
            "message": "Message is required"
        }), 400

    # Get AI response
    response = assistant.get_financial_advice(message)
    return jsonify(response)

@app.route('/api/invest', methods=['POST'])
def investment_advice():
    """Get investment advice"""
    data = request.get_json()
    amount = data.get('amount', 0)
    risk = data.get('risk_level', 'medium')

    # Validate amount
    valid, value = validate_amount(amount)
    if not valid:
        return jsonify({
            "status": "error",
            "message": value
        }), 400

    response = assistant.get_investment_advice(
        value, risk
    )
    return jsonify(response)

# ==================
# EXPENSE ROUTES
# ==================

@app.route('/api/expense/add', methods=['POST'])
def add_expense():
    """Add new expense"""
    data = request.get_json()
    category = data.get('category', 'Other')
    amount = data.get('amount', 0)
    description = data.get('description', '')

    # Validate amount
    valid, value = validate_amount(amount)
    if not valid:
        return jsonify({
            "status": "error",
            "message": value
        }), 400

    result = tracker.add_expense(
        category, value, description
    )

    # Update AI context
    assistant.update_context(
        expense={
            "category": category,
            "amount": value
        }
    )

    return jsonify(result)

@app.route('/api/expense/summary', methods=['GET'])
def expense_summary():
    """Get expense summary"""
    summary = tracker.get_summary()

    if summary["status"] == "success":
        # Add financial health
        savings_rate = calculate_savings_rate(
            summary["income"],
            summary["total_expenses"]
        )
        summary["savings_rate"] = savings_rate
        summary["health"] = get_financial_health(
            savings_rate
        )

    return jsonify(summary)

@app.route('/api/income/set', methods=['POST'])
def set_income():
    """Set monthly income"""
    data = request.get_json()
    income = data.get('income', 0)

    valid, value = validate_amount(income)
    if not valid:
        return jsonify({
            "status": "error",
            "message": value
        }), 400

    result = tracker.set_income(value)
    assistant.update_context(income=value)
    return jsonify(result)

@app.route('/api/budget/analyze', methods=['POST'])
def analyze_budget():
    """Analyze budget with AI"""
    data = request.get_json()
    income = data.get('income', tracker.income)
    expenses = tracker.expenses

    if not expenses:
        return jsonify({
            "status": "error",
            "message": "No expenses to analyze"
        }), 400

    result = assistant.calculate_budget(
        income, expenses
    )
    return jsonify(result)

# ==================
# CURRENCY ROUTES
# ==================

@app.route('/api/currency/convert',
           methods=['POST'])
def convert_currency():
    """Convert currency"""
    data = request.get_json()
    amount = data.get('amount', 0)
    from_cur = data.get('from', 'USD')
    to_cur = data.get('to', 'EUR')

    valid, value = validate_amount(amount)
    if not valid:
        return jsonify({
            "status": "error",
            "message": value
        }), 400

    result = google_services.convert_currency(
        value, from_cur, to_cur
    )
    return jsonify(result)

@app.route('/api/currency/rates', methods=['GET'])
def get_rates():
    """Get currency rates"""
    base = request.args.get('base', 'USD')
    result = google_services.get_multiple_rates(base)
    return jsonify(result)

# ==================
# ANALYSIS ROUTES
# ==================

@app.route('/api/analyze/expenses',
           methods=['POST'])
def analyze_expenses():
    """Analyze expenses with AI"""
    expenses = tracker.expenses

    if not expenses:
        return jsonify({
            "status": "error",
            "message": "No expenses to analyze"
        }), 400

    result = assistant.analyze_expenses(expenses)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
