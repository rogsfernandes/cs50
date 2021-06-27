from core.domain.stock import Stock
from core.domain.transaction import Transaction
from core.services.stock_service import StockService
from server.database.sqlite import db


class TransactionService:
    def register(self, user_id, symbol, price, shares, type):
        # Register user share
        total = shares * price
        user_shares = db.execute("SELECT * FROM users_shares WHERE user_id = ?", user_id)
        is_update = False

        for share in user_shares:
            if share["symbol"] == symbol:
                is_update = True
                updated_shares = int(share["shares"]) + shares if type == "BUY" else int(share["shares"]) - shares
                if updated_shares == 0:
                    db.execute("DELETE FROM users_shares WHERE user_id = ? AND symbol = ?", user_id, symbol)
                else:
                    db.execute("UPDATE users_shares SET shares = ? WHERE user_id = ? AND symbol = ?", updated_shares,
                               user_id, symbol)

        if not is_update and type == "BUY":
            db.execute("INSERT INTO users_shares (user_id, symbol, shares) VALUES (?, ?, ?)", user_id, symbol,
                       shares)

        if len(user_shares) == 0:
            db.execute("INSERT INTO users_shares (user_id, symbol, shares) VALUES (?, ?, ?)", user_id, symbol,
                       shares)

        # Register transaction
        rows = db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, total, type) values (?, ?, ?, ?, ?, ?)",
            user_id,
            symbol,
            shares,
            price,
            total,
            type)
        return rows > 0

    def get_by_user(self, user_id):
        rows = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
        stock_service = StockService()
        transactions = [Transaction(
            stock_service.get(row["symbol"]),
            row["shares"],
            row["total"],
            row["type"]
        ) for row in rows]

        for t in transactions:
            print(t.stock.symbol)

        return transactions
