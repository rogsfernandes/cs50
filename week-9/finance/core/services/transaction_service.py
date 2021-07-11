from core.domain.stock import Stock
from core.domain.transaction import Transaction
from core.services.stock_service import StockService
from core.services.user_service import UserService
from server.database.sqlite import db


class TransactionService:
    def register_buy(self, user_id, symbol, price, shares, type):
        # Register user share
        total = shares * price
        self.validate_buy(user_id, total)
        user_shares = db.execute("SELECT * FROM users_shares WHERE user_id = ?", user_id)

        is_update = False
        for share in user_shares:
            if share["symbol"] == symbol:
                is_update = True
                updated_shares = int(share["shares"]) + shares
                db.execute("UPDATE users_shares SET shares = ? WHERE user_id = ? AND symbol = ?", updated_shares,
                           user_id, symbol)

        if not is_update:
            db.execute("INSERT INTO users_shares (user_id, symbol, shares) VALUES (?, ?, ?)", user_id, symbol,
                       shares)
        user_service = UserService()
        user_service.subtract_cash(user_id, total)
        return self.register(user_id, symbol, price, shares, total, type)

    def validate_buy(self, user_id, total):
        user_service = UserService()
        user = user_service.get_by_id(user_id)
        if total > user.cash:
            raise ValueError('Not enough money')

    def register_sell(self, user_id, symbol, price, quantity, type):
        # Register user share
        total = quantity * price
        user_shares = db.execute("SELECT * FROM users_shares WHERE user_id = ?", user_id)

        for share in user_shares:
            if share["symbol"] == symbol:
                shares = int(share["shares"])
                self.validate_sell(shares, quantity)
                updated_shares = shares - quantity
                if updated_shares == 0:
                    db.execute("DELETE FROM users_shares WHERE user_id = ? AND symbol = ?", user_id, symbol)
                else:
                    db.execute("UPDATE users_shares SET shares = ? WHERE user_id = ? AND symbol = ?", updated_shares,
                               user_id, symbol)
        user_service = UserService()
        user_service.add_cash(user_id, total)
        return self.register(user_id, symbol, price, quantity, total, type)

    def validate_sell(self, shares, quantity):
        if quantity > shares:
            print(f'Error trying to sell shares: user has {shares} shares and tried to sell {quantity}')
            raise ValueError('Not enough shares to sell')

    def register(self, user_id, symbol, price, shares, total, type):
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
