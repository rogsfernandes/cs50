from flask import session, render_template

from core.services.stock_service import StockService
from core.services.transaction_service import TransactionService
from core.services.user_service import UserService
from helpers import apology


def buy_stock(request):
    stock_service = StockService()
    stock = stock_service.get(request.form.get("symbol"))

    # Validate symbol
    if not request.form.get("symbol") or not stock:
        return apology("Symbol not found!")
    # Validate shares number
    if not request.form.get("shares") or int(request.form.get("shares")) < 0:
        return apology("Number of shares must be a positive number.")

    shares = int(request.form.get("shares"))
    id = session["user_id"]
    user_service = UserService()
    transaction_service = TransactionService()

    # Gets user available cash
    try:
        transaction_service.register(id, stock.symbol, stock.price, shares, "BUY")
        user = user_service.get_by_id(id)
        user.set_shares(user_service.get_shares(user.id))
        return render_template("index.html", user=user)
    except ValueError:
        return apology("Not enough money!")


def sell_stock(request):
    user_id = session["user_id"]
    user_service = UserService()
    user = user_service.get_by_id(user_id)
    user.set_shares(user_service.get_shares(user.id))

    found = False
    for share in user.shares:
        if share.stock.symbol == request.form.get("symbol") and share.number >= int(request.form.get("shares")):
            found = True
            transaction_service = TransactionService()
            transaction_service.register(user.id, request.form.get("symbol"), share.stock.price,
                                         int(request.form.get("shares")), "SELL")

            user = user_service.get_by_id(user_id)
            user.set_shares(user_service.get_shares(user.id))
            return user

    if not found:
        raise ValueError
