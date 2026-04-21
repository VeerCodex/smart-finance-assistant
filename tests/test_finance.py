import unittest
import json
from app import app
from src.utils import (validate_amount,
                       calculate_savings_rate,
                       get_financial_health)
from src.expense_tracker import ExpenseTracker

class TestFinanceAssistant(unittest.TestCase):

    def setUp(self):
        """Setup test client"""
        self.client = app.test_client()
        self.tracker = ExpenseTracker()

    # ==================
    # API TESTS
    # ==================

    def test_home_loads(self):
        """Test home page"""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

    def test_health_check(self):
        """Test health endpoint"""
        res = self.client.get('/health')
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'healthy')

    def test_chat_valid(self):
        """Test valid chat message"""
        res = self.client.post('/api/chat',
            json={'message': 'How to save money?'},
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)

    def test_chat_empty(self):
        """Test empty message returns 400"""
        res = self.client.post('/api/chat',
            json={'message': ''},
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_set_income(self):
        """Test setting income"""
        res = self.client.post('/api/income/set',
            json={'income': 5000},
            content_type='application/json'
        )
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'success')

    def test_add_expense(self):
        """Test adding expense"""
        res = self.client.post('/api/expense/add',
            json={
                'category': 'Food',
                'amount': 200,
                'description': 'Groceries'
            },
            content_type='application/json'
        )
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'success')

    def test_invalid_amount(self):
        """Test invalid amount returns 400"""
        res = self.client.post('/api/expense/add',
            json={
                'category': 'Food',
                'amount': 'invalid'
            },
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    # ==================
    # UNIT TESTS
    # ==================

    def test_validate_amount_valid(self):
        """Test valid amount"""
        valid, value = validate_amount(100)
        self.assertTrue(valid)
        self.assertEqual(value, 100.0)

    def test_validate_amount_negative(self):
        """Test negative amount"""
        valid, msg = validate_amount(-50)
        self.assertFalse(valid)

    def test_validate_amount_string(self):
        """Test string amount"""
        valid, msg = validate_amount("abc")
        self.assertFalse(valid)

    def test_savings_rate(self):
        """Test savings rate calculation"""
        rate = calculate_savings_rate(5000, 4000)
        self.assertEqual(rate, 20.0)

    def test_financial_health_excellent(self):
        """Test excellent health status"""
        health = get_financial_health(25)
        self.assertIn("Excellent", health['status'])

    def test_financial_health_poor(self):
        """Test poor health status"""
        health = get_financial_health(-10)
        self.assertIn("Poor", health['status'])

    def test_expense_tracker_add(self):
        """Test expense tracker"""
        result = self.tracker.add_expense(
            "Food", 100, "Lunch"
        )
        self.assertEqual(result['status'], 'success')

    def test_expense_tracker_summary(self):
        """Test expense summary"""
        self.tracker.add_expense("Food", 200)
        self.tracker.add_expense("Transport", 100)
        summary = self.tracker.get_summary()
        self.assertEqual(
            summary['total_expenses'], 300.0
        )

if __name__ == '__main__':
    unittest.main()
