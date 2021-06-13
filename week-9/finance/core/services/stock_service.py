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
            # Check whether we already have this stock in our database
            rows = db.execute("SELECT * FROM stocks WHERE symbol = ?", quote["symbol"])

            if len(rows) == 0:
                # Register if stock is new
                db.execute("INSERT INTO stocks(name, symbol) VALUES(?, ?)", quote["companyName"], quote["symbol"])
                rows = db.execute("SELECT * FROM stocks WHERE symbol = ?", quote["symbol"])

            stock = Stock(rows[0]["id"], rows[0]["name"], rows[0]["symbol"], float(quote["latestPrice"]))
            return stock
        except (KeyError, TypeError, ValueError):
            return None
