from core.domain.stock import Stock
from core.domain.transaction import Transaction
from core.services.stock import StockService
from server.database.sqlite import db


class TransactionService:
    def register(self, user_id, symbol, quantity, price):
        stock_service = StockService()
        stock = stock_service.get(symbol)
        total = quantity * stock.price
        rows = db.execute("INSERT INTO transactions (user_id, stock_id, quantity, price, total) values (?, ?, ?, ?, ?)",
                          user_id,
                          symbol,
                          quantity,
                          stock.price,
                          total)
        return rows > 0

    def get_by_user_and_symbol(self, user, symbol):
        rows = db.execute("SELECT * FROM transactions WHERE user_id = ? AND symbol = ?;", user.id, symbol)
        transactions = [Transaction(Stock(row["name"], row["symbol"], row["price"]), row["quantity"], row["total"],
                                    row["average_price"]) for row in rows]

        return transactions
