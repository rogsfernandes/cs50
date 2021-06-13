from werkzeug.security import generate_password_hash

from core.domain.portfolio import Portfolio
from core.domain.user import User
from core.services.portfolio_service import PortfolioService
from server.database.sqlite import db


class UserService:
    def get_by_id(self, id):
        return self.__get_by("id", id)

    def get_by_username(self, username):
        return self.__get_by("username", username)

    def __get_by(self, property, value):
        rows = db.execute(f"SELECT * FROM users WHERE {property} = ?", value)
        if len(rows) > 0:
            row = rows[0]
            return User(row["id"], row["username"], row["cash"], row["hash"])
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

    def get_portfolio(self, user_id):
        user = self.get_by_id(user_id)
        portfolio_service = PortfolioService()
        portfolio = portfolio_service.get(user)
        return portfolio