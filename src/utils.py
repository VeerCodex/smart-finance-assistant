def format_currency(amount, currency="USD"):
    """Format amount as currency"""
    symbols = {
        "USD": "$", "EUR": "€",
        "GBP": "£", "INR": "₹",
        "JPY": "¥"
    }
    symbol = symbols.get(currency, "$")
    return f"{symbol}{amount:,.2f}"

def calculate_savings_rate(income, expenses):
    """Calculate savings rate percentage"""
    if income <= 0:
        return 0
    savings = income - expenses
    return round((savings / income) * 100, 1)

def get_financial_health(savings_rate):
    """Get financial health status"""
    if savings_rate >= 20:
        return {
            "status": "Excellent 🟢",
            "message": "Great savings rate!"
        }
    elif savings_rate >= 10:
        return {
            "status": "Good 🟡",
            "message": "Try to save more"
        }
    elif savings_rate >= 0:
        return {
            "status": "Fair 🟠",
            "message": "Reduce expenses"
        }
    else:
        return {
            "status": "Poor 🔴",
            "message": "Spending more than earning!"
        }

def validate_amount(amount):
    """Validate monetary amount"""
    try:
        value = float(amount)
        if value < 0:
            return False, "Amount cannot be negative"
        return True, value
    except (ValueError, TypeError):
        return False, "Invalid amount"
