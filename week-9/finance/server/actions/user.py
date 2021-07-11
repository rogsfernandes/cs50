from flask import redirect, render_template
from werkzeug.security import check_password_hash

from core.services.transaction_service import TransactionService
from core.services.user_service import UserService
from helpers import apology


def register_user(request, session):
    # Ensure username was submitted
    if not request.form.get("username"):
        return apology("must provide username", 400)

    # Ensure password was submitted
    if not request.form.get("password"):
        return apology("must provide password", 400)

    # Ensure confirmation is equal password
    if request.form.get("password") != request.form.get("confirmation"):
        return apology("password and confirmation doesn't match", 400)

    user_service = UserService()

    if user_service.get_by_username(request.form.get("username")):
        return apology("username already exists", 400)

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
    if not request.form.get("password"):
        return apology("must provide password", 403)

    user_service = UserService()
    # Query database for username
    user = user_service.get_by_username(request.form.get("username"))
    if not user:
        return apology("invalid username and/or password", 403)

    # Ensure username exists and password is correct
    if not check_password_hash(user.get_hash(), request.form.get("password")):
        return apology("invalid username and/or password", 403)

    user.set_shares(user_service.get_shares(user.id))

    # Remember which user has logged in
    session["user_id"] = user.id
    return redirect("/")


def get_user(session):
    user_id = session["user_id"]
    user_service = UserService()
    user = user_service.get_by_id(user_id)
    user.set_shares(user_service.get_shares(user.id))
    return user


def get_transactions(session):
    user_id = session["user_id"]
    transaction_service = TransactionService()
    transactions = transaction_service.get_by_user(user_id)
    return transactions
