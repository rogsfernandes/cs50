from werkzeug.security import generate_password_hash

from core.domain.user import User
from server.database.sqlite import db


class UserService:
    def get(self, id):
        rows = db.execute("SELECT * FROM users WHERE id = ?", id)
        if len(rows) > 0:
            row = rows[0]
            return User(row["id"], row["username"], row["cash"])
        else:
            return rows

    def register(self, username, password):
        # Validates if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return []

        # Generate password hash
        hash = generate_password_hash(password)

        # Register user
        result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        if result:
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            return rows
