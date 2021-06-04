from werkzeug.security import check_password_hash
from flask import redirect

from core.services.user import UserService
from helpers import apology
from server.database.sqlite import db


def register_user(request, session):
    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 403)

    # Ensure password was submitted
    if not request.form.get("password"):
        return apology("must provide password", 403)

    # Ensure confirmation is equal password
    if request.form.get("password") != request.form.get("confirmation"):
        return apology("password and confirmation doesn't match", 403)

    user_service = UserService()
    rows = user_service.register(request.form.get("username"), request.form.get("password"))

    if len(rows) > 0:
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
