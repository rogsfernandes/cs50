from werkzeug.security import check_password_hash
from flask import redirect

from core.services.portfolio_service import PortfolioService
from core.services.stock_service import StockService
from core.services.user_service import UserService
from server.helpers import apology
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

    user_service = UserService()
    # Query database for username
    user = user_service.get_by_username(request.form.get("username"))

    # Ensure username exists and password is correct
    if not check_password_hash(user.hash, request.form.get("password")):
        return apology("invalid username and/or password", 403)

    # Remember which user has logged in
    session["user_id"] = user.id

    # Redirect user to home page
    return redirect("/")


def get_portfolio(session):
    user_id = session["user_id"]
    user_service = UserService()

    portfolio = user_service.get_portfolio(user_id)

    return portfolio

