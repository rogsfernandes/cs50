import os
import urllib

import requests

from core.domain.stock import Stock
from server.database.sqlite import db


class StockService:
    def get(self, symbol):
        """Look up quote for symbol."""

        # Contact API to get latest price
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
            stock = Stock(quote["companyName"], quote["symbol"], float(quote["latestPrice"]))
            # Check whether we already have this stock in our database
            rows = db.execute("SELECT * FROM stocks WHERE symbol = ?", stock.symbol)
            if len(rows) > 0:
                return stock
            else:
                # Register if stock is new
                db.execute("INSERT INTO stocks(name, symbol) VALUES(?, ?)", stock.name, stock.symbol)
                return stock
        except (KeyError, TypeError, ValueError):
            return None


