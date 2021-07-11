from flask import session, render_template

from core.services.stock_service import StockService
from core.services.transaction_service import TransactionService
from core.services.user_service import UserService
from helpers import apology


def buy_stock(symbol, shares):
    stock_service = StockService()
    stock = stock_service.get(symbol)

    if not stock:
        return apology("Invalid Stock")

    shares = int(shares)
    id = session["user_id"]
    transaction_service = TransactionService()

    # Gets user available cash
    transaction_service.register_buy(id, stock.symbol, stock.price, shares, "BUY")


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
            transaction_service.register_sell(user.id, request.form.get("symbol"), share.stock.price,
                                              int(request.form.get("shares")), "SELL")

            user = user_service.get_by_id(user_id)
            user.set_shares(user_service.get_shares(user.id))
            return user

    if not found:
        raise ValueError
