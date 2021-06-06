from flask import session
from werkzeug.utils import redirect

from core.services.stock import StockService
from core.services.user import UserService
from helpers import apology, lookup

def buy_stock(request):
    # Validate symbol
    if not request.form.get("symbol") or not lookup(request.form.get("symbol")):
        return apology("Symbol not found!")
    # Validate shares number
    if not request.form.get("shares") or int(request.form.get("shares")) < 0:
        return apology("Shares quantity must be a positive number.")

    quote = lookup(request.form.get("symbol"))
    shares = int(request.form.get("shares"))
    id = session["user_id"]
    user_service = UserService()
    stock_service = StockService()

    # Gets user available cash
    user = user_service.get(id)
    success = stock_service.buy(user.id, quote["symbol"], shares, quote["price"])

    if success:
        return redirect("/")
    else:
        return apology("Not enough money!")