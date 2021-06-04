from helpers import apology, lookup


def buy_stock(request):
    # Validate symbol
    if not request.form.get("symbol") or not lookup(request.form.get("symbol")):
        return apology("Symbol not found!")
    # Validate shares number
    if not request.form.get("shares") or int(request.form.get("shares")) < 0:
        return apology("Shares quantity must be a positive number.")

    symbol = request.form.get("symbol")
    shares = request.form.get("shares")

    return apology("Not implemented!")