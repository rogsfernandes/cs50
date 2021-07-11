import os
from tempfile import mkdtemp

from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash

from core.services.stock_service import StockService
from server.actions.stock import buy_stock, sell_stock
from server.actions.user import register_user, get_user, get_transactions
from helpers import apology, login_required, usd

# Configure application
from server.database.sqlite import db

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Get User's data"""
    user = get_user(session)
    return render_template("index.html", user=user)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Validate symbol
        if not request.form.get("symbol"):
            return apology("Symbol not found!")
        # Validate shares number
        if not request.form.get("shares") or int(request.form.get("shares")) < 0:
            return apology("Number of shares must be a positive number.")

        try:
            buy_stock(request.form.get("symbol"), request.form.get("shares"))
            return redirect("/")
        except ValueError:
            return apology("Not possible!")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = get_transactions(session)
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Quote the value of a stock"""
    if request.method == "POST":
        stock_service = StockService()
        stock = stock_service.get(request.form.get("symbol"))
        if not stock:
            return apology("Invalid Stock!", 400)
        else:
            return render_template("quoted.html", quote=stock)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation is equal password
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation doesn't match", 400)

        """Register user"""
        if request.method == "POST":
            user = register_user(request.form.get("username"), request.form.get("password"))
            if not user:
                return apology("Not possible to register, possibly duplicate", 400)
            else:
                session["user_id"] = user.id
                return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        try:
            user = sell_stock(request)
            return render_template("index.html", user=user)
        except ValueError:
            return apology("No shares to sell")
    else:
        user = get_user(session)
        return render_template("sell.html", shares=user.shares)


def error_handler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(error_handler)
