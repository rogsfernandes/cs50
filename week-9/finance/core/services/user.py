from werkzeug.security import generate_password_hash

from server.database.sqlite import db


class UserService:
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
