from flask import session
from werkzeug.utils import redirect

from core.services.stock_service import StockService
from core.services.transaction_service import TransactionService
from core.services.user_service import UserService
from server.helpers import apology

def buy_stock(request):
    stock_service = StockService()
    stock = stock_service.get(request.form.get("symbol"))

    # Validate symbol
    if not request.form.get("symbol") or not stock:
        return apology("Symbol not found!")
    # Validate shares number
    if not request.form.get("shares") or int(request.form.get("shares")) < 0:
        return apology("Shares quantity must be a positive number.")

    shares = int(request.form.get("shares"))
    id = session["user_id"]
    user_service = UserService()
    transaction_service = TransactionService()

    # Gets user available cash
    user = user_service.get_by_id(id)
    success = transaction_service.register(user.id, stock.symbol, shares, "BUY")

    if success:
        return redirect("/")
    else:
        return apology("Not enough money!")

# def sell_stock(request):
