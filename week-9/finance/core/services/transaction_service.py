from core.domain.stock import Stock
from core.domain.transaction import Transaction
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
                db.execute("UPDATE users_shares SET shares = ? WHERE user_id = ?", updated_shares, user_id)

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

    def get_by_user_and_symbol(self, user, symbol):
        rows = db.execute("SELECT * FROM transactions WHERE user_id = ? AND symbol = ?;", user.id, symbol)
        transactions = [Transaction(Stock(
            row["name"],
            row["symbol"],
            row["price"]),
            row["shares"],
            row["total"],
            row["average_price"],
            row["type"]) for row in rows]

        return transactions
