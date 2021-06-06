from flask import session
from werkzeug.utils import redirect

from core.services.stock import StockService
from core.services.user import UserService
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

    # Gets user available cash
    user = user_service.get(id)
    success = stock_service.buy(user.id, stock.symbol, shares, stock.price)

    if success:
        return redirect("/")
    else:
        return apology("Not enough money!")