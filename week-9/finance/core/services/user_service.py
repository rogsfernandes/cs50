from werkzeug.security import generate_password_hash

from core.domain.shares import Share
from core.domain.user import User
from core.services.stock_service import StockService
from server.database.sqlite import db


class UserService:
    def get_by_id(self, id):
        return self.__get_by("id", id)

    def get_by_username(self, username):
        return self.__get_by("username", username)

    def __get_by(self, property, value):
        rows = db.execute(
            f"SELECT * FROM users WHERE {property} = ?", value
        )
        # Get user shares
        if len(rows) > 0:
            return User(rows[0]["id"], rows[0]["username"], rows[0]["cash"], rows[0]["hash"], [])
        else:
            return None

    def register(self, username, password):
        # Validates if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return None

        # Generate password hash
        hash = generate_password_hash(password)

        # Register user
        result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        if result:
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            return rows
        else:
            return None

    def get_shares(self, user_id):
        stock_service = StockService()
        rows = db.execute(
            f"SELECT * FROM users JOIN users_shares on users.id = users_shares.user_id WHERE user_id = ?", user_id
        )
        shares = [Share(stock_service.get(row["symbol"]), row["shares"]) for row in rows]
        return shares

    def add_cash(self, user_id, amount):
        user = self.get_by_id(user_id)
        db.execute("UPDATE users SET cash = ?", user.cash + amount)

    def subtract_cash(self, user_id, amount):
        user = self.get_by_id(user_id)
        db.execute("UPDATE users SET cash = ?", user.cash - amount)
