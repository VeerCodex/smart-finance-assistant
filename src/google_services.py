import requests
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleServices:
    def __init__(self):
        self.exchange_key = os.getenv("EXCHANGE_API_KEY")
        self.sheets_id = os.getenv("GOOGLE_SHEETS_ID")

    def get_exchange_rate(self, from_currency, to_currency):
        """Get real-time currency exchange rates"""
        try:
            url = f"https://v6.exchangerate-api.com/v6/{self.exchange_key}/pair/{from_currency}/{to_currency}"
            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get("result") == "success":
                return {
                    "status": "success",
                    "from": from_currency,
                    "to": to_currency,
                    "rate": data["conversion_rate"],
                    "time": data["time_last_update_utc"]
                }
            return {
                "status": "error",
                "message": "Could not fetch rate"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def convert_currency(self, amount,
                        from_currency,
                        to_currency):
        """Convert currency amount"""
        rate_data = self.get_exchange_rate(
            from_currency,
            to_currency
        )

        if rate_data["status"] == "success":
            converted = amount * rate_data["rate"]
            return {
                "status": "success",
                "original": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "converted": round(converted, 2),
                "rate": rate_data["rate"]
            }
        return rate_data

    def get_multiple_rates(self, base_currency="USD"):
        """Get multiple currency rates"""
        try:
            url = f"https://v6.exchangerate-api.com/v6/{self.exchange_key}/latest/{base_currency}"
            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get("result") == "success":
                # Return popular currencies
                popular = ["EUR", "GBP", "JPY",
                          "INR", "AUD", "CAD",
                          "CHF", "CNY", "SGD"]

                rates = {}
                for currency in popular:
                    if currency in data["conversion_rates"]:
                        rates[currency] = data[
                            "conversion_rates"
                        ][currency]

                return {
                    "status": "success",
                    "base": base_currency,
                    "rates": rates
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
