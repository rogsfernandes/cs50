from server.database.sqlite import db


class StockService:
    def buy(self, user_id, symbol, quantity, price):
        total = quantity * price
        rows = db.execute("INSERT INTO transactions (user_id, symbol, quantity, price, total) values (?, ?, ?, ?, ?)",
                          user_id,
                          symbol,
                          quantity,
                          price,
                          total)
        return rows > 0