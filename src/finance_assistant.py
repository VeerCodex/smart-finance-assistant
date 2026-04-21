import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class FinanceAssistant:
    def __init__(self):
        """Initialize Gemini AI for Finance"""
        genai.configure(
            api_key=os.getenv("GEMINI_API_KEY")
        )
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat_history = []
        self.user_context = {
            "income": None,
            "expenses": [],
            "savings_goal": None,
            "currency": "USD"
        }

    def get_financial_advice(self, user_input):
        """Get smart financial advice"""
        prompt = f"""
        You are an expert financial advisor assistant.
        
        User Financial Context:
        - Monthly Income: {self.user_context['income']}
        - Recent Expenses: {self.user_context['expenses'][-3:] if self.user_context['expenses'] else 'None'}
        - Savings Goal: {self.user_context['savings_goal']}
        - Currency: {self.user_context['currency']}
        
        Chat History (last 3):
        {self.chat_history[-3:] if self.chat_history else 'None'}
        
        User Question: {user_input}
        
        Provide:
        1. Clear financial advice
        2. Specific actionable steps
        3. Budget recommendations if needed
        4. Savings tips if relevant
        5. Risk warnings if applicable
        
        Keep response clear, helpful and professional.
        """

        try:
            response = self.model.generate_content(prompt)
            
            # Save to history
            self.chat_history.append({
                "user": user_input,
                "assistant": response.text
            })
            
            return {
                "status": "success",
                "response": response.text,
                "type": "advice"
            }
        except Exception as e:
            return {
                "status": "error",
                "response": f"Error: {str(e)}",
                "type": "error"
            }

    def analyze_expenses(self, expenses):
        """Analyze user expenses with AI"""
        expense_list = "\n".join([
            f"- {exp['category']}: ${exp['amount']}"
            for exp in expenses
        ])

        prompt = f"""
        Analyze these monthly expenses and provide insights:
        
        {expense_list}
        
        Provide:
        1. Spending pattern analysis
        2. Areas to cut costs
        3. Budget allocation advice (50/30/20 rule)
        4. Savings recommendations
        5. Financial health score (1-10)
        
        Be specific and actionable.
        """

        try:
            response = self.model.generate_content(prompt)
            return {
                "status": "success",
                "analysis": response.text
            }
        except Exception as e:
            return {
                "status": "error",
                "analysis": str(e)
            }

    def get_investment_advice(self, amount, risk_level):
        """Get investment recommendations"""
        prompt = f"""
        Provide investment advice for:
        - Investment Amount: ${amount}
        - Risk Level: {risk_level} (low/medium/high)
        
        Recommend:
        1. Best investment options
        2. Portfolio allocation
        3. Expected returns
        4. Risk factors
        5. Time horizon
        
        Include both traditional and modern options.
        Always mention: "Consult a financial advisor"
        """

        try:
            response = self.model.generate_content(prompt)
            return {
                "status": "success",
                "advice": response.text
            }
        except Exception as e:
            return {
                "status": "error",
                "advice": str(e)
            }

    def calculate_budget(self, income, expenses):
        """Calculate smart budget plan"""
        total_expenses = sum(
            exp['amount'] for exp in expenses
        )
        savings = income - total_expenses
        savings_percent = (savings / income * 100) if income > 0 else 0

        prompt = f"""
        Create a budget plan for:
        - Monthly Income: ${income}
        - Total Expenses: ${total_expenses}
        - Current Savings: ${savings} ({savings_percent:.1f}%)
        
        Provide:
        1. Budget health assessment
        2. Recommended 50/30/20 budget
        3. Specific savings targets
        4. Emergency fund advice
        5. Next steps to improve finances
        """

        try:
            response = self.model.generate_content(prompt)
            return {
                "status": "success",
                "income": income,
                "total_expenses": total_expenses,
                "savings": savings,
                "savings_percent": round(savings_percent, 1),
                "ai_advice": response.text
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def update_context(self, income=None,
                      expense=None,
                      savings_goal=None):
        """Update user financial context"""
        if income:
            self.user_context['income'] = income
        if expense:
            self.user_context['expenses'].append(expense)
        if savings_goal:
            self.user_context['savings_goal'] = savings_goal
