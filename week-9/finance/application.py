import os
from tempfile import mkdtemp

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from core.domain.shares import Share
from core.domain.stock import Stock
from core.domain.transaction import Transaction
from core.domain.user import User
from core.services.stock_service import StockService
from helpers import apology, login_required, usd, lookup

# Configure application
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

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Get User's data"""
    user_id = session["user_id"]
    rows = db.execute("SELECT * FROM users where id = ?", user_id)
    user = User(rows[0]["id"], rows[0]["username"], rows[0]["cash"], rows[0]["hash"], [])

    stock_service = StockService()
    rows = db.execute(
        f"SELECT * FROM users JOIN users_shares on users.id = users_shares.user_id WHERE user_id = ?", user_id
    )
    shares = [Share(stock_service.get(row["symbol"]), row["shares"]) for row in rows]
    user.set_shares(shares)

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

        try:
            if not request.form.get("shares") or int(request.form.get("shares")) < 0:
                return apology("Number of shares must be a positive integer.")
        except ValueError:
                return apology("Number of shares must be a positive integer.")

        stock_service = StockService()
        stock = stock_service.get(request.form.get("symbol"))

        if not stock:
            return apology("Stock not found!")

        user_id = session["user_id"]
        shares = int(request.form.get("shares"))
        symbol = request.form.get("symbol")
        price = stock.price
        amount = shares * stock.price

        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        cash = float(rows[0]["cash"])

        if cash < amount:
            return apology("Transaction value is bigger than available money")

        rows = db.execute("SELECT * FROM users_shares WHERE user_id = ?", user_id)
        user_shares = [Share(stock_service.get(row["symbol"]), row["shares"]) for row in rows]
        is_update = False

        # Check if user already has shares of this stock
        for share in user_shares:
            if share.stock.symbol == symbol:
                is_update = True
                updated_shares = int(share["shares"]) + shares
                db.execute("UPDATE users_shares SET shares = ? WHERE user_id = ? AND symbol = ?", updated_shares,
                           user_id, symbol)

        # Insert new share for the user if it's a new share for they
        if not is_update:
            db.execute("INSERT INTO users_shares (user_id, symbol, shares) VALUES (?, ?, ?)", user_id, symbol, shares)

        # Subtract from user's cash
        db.execute("UPDATE users SET cash = ?", cash - amount)

        # Register transaction
        rows = db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, total, type) values (?, ?, ?, ?, ?, ?)",
            user_id,
            symbol,
            shares,
            price,
            amount,
            "BUY")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    rows = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    stock_service = StockService()
    transactions = [Transaction(
        stock_service.get(row["symbol"]),
        row["shares"],
        row["total"],
        row["type"]
    ) for row in rows]
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
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Invalid Stock!", 400)
        else:
            stock = Stock(quote["name"], quote["symbol"], quote["price"])
            return render_template("quoted.html", quote=stock)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
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

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) > 0:
            return apology("Username already exists", 400)

        # Generate password hash
        hash = generate_password_hash(request.form.get("password"))

        # Register user
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hash)

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Validate symbol
        if not request.form.get("symbol"):
            return apology("Symbol not found!")

        stock_service = StockService()
        stock = stock_service.get(request.form.get("symbol"))

        # Validate shares number
        if not stock:
            return apology("Stock not found!")

        try:
            user_id = session["user_id"]
            quantity = int(request.form.get("shares"))
            symbol = request.form.get("symbol")
            price = stock.price
            amount = quantity * stock.price

            rows = db.execute("SELECT * FROM users_shares WHERE user_id = ?", user_id)
            user_shares = [Share(stock_service.get(row["symbol"]), row["shares"]) for row in rows]

            if len(user_shares) == 0:
                return apology("No shares to sell")

            for share in user_shares:
                if share.stock.symbol == request.form.get("symbol"):
                    if share.number < quantity:
                        return apology(f"You have {share.number} available for selling.")
                    updated_shares = share.number - quantity
                    if updated_shares == 0:
                        db.execute("DELETE FROM users_shares WHERE user_id = ? AND symbol = ?", user_id, request.form.get("symbol"))
                    else:
                        db.execute("UPDATE users_shares SET shares = ? WHERE user_id = ? AND symbol = ?", updated_shares, user_id, request.form.get("symbol"))

            rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
            # Add money to user's cash
            db.execute("UPDATE users SET cash = ?", float(rows[0]["cash"]) + amount)

            # Register transaction
            rows = db.execute(
                "INSERT INTO transactions (user_id, symbol, shares, price, total, type) values (?, ?, ?, ?, ?, ?)",
                user_id,
                symbol,
                quantity,
                price,
                amount,
                "SELL")

            return redirect("/")
        except ValueError:
            return apology("Something went wront")
    else:
        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM users_shares WHERE user_id = ?", user_id)
        shares = [Share(Stock(None, row["symbol"], 0), row["shares"]) for row in rows]
        return render_template("sell.html", shares=shares)


def error_handler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(error_handler)
