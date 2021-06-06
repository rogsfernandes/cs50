import os
import urllib

import requests

from core.domain.stock import Stock
from server.database.sqlite import db


class StockService:
    def get(self, symbol):
        """Look up quote for symbol."""

        # Contact API
        try:
            api_key = os.environ.get("API_KEY")
            url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException:
            return None

        # Parse response
        try:
            quote = response.json()
            return Stock(quote["companyName"], quote["symbol"], float(quote["latestPrice"]))
        except (KeyError, TypeError, ValueError):
            return None

    def buy(self, user_id, symbol, quantity, price):
        total = quantity * price
        rows = db.execute("INSERT INTO transactions (user_id, symbol, quantity, price, total) values (?, ?, ?, ?, ?)",
                          user_id,
                          symbol,
                          quantity,
                          price,
                          total)
        return rows > 0