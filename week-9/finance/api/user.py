from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect

from database.sqlite import db
from helpers import apology


def register_user(request, session):
    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 403)

    # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 403)

    # Ensure confirmation is equal password
    elif request.form.get("password") != request.form.get("confirmation"):
        return apology("password and confirmation doesn't match", 403)

    else:
        # Validates if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))
        if len(rows) > 0:
            return apology("Username already exists")

    # Generate password hash
    hash = generate_password_hash(request.form.get("password"))

    # Register user
    result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                        request.form.get("username"), hash)

    if result:
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return apology("Something went wrong")


def signin(request, session):
    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 403)

    # Ensure password was submitted
    elif not request.form.get("password"):
        return apology("must provide password", 403)

    # Query database for username
    rows = db.execute("SELECT * FROM users WHERE username = ?",
                      request.form.get("username"))

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        return apology("invalid username and/or password", 403)

    # Remember which user has logged in
    session["user_id"] = rows[0]["id"]

    # Redirect user to home page
    return redirect("/")
