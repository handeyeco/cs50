from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    user = db.execute("SELECT * FROM users WHERE (id=:user_id)", user_id=session["user_id"])[0]
    transactions = db.execute("SELECT * FROM transactions JOIN stocks ON transactions.stock_id = stocks.id WHERE transactions.user_id = :user_id", user_id=session["user_id"])
    portfolio = {}
    for tx in transactions:
        symbol = tx['symbol']
        if symbol in portfolio:
            if tx['buy'] == 1:
                portfolio[symbol]['count'] += tx['count']
            else:
                portfolio[symbol]['count'] -= tx['count']
        else:
            tx['price'] = lookup(symbol)['price']
            portfolio[symbol] = tx

    user['value'] = user['cash']
    for symbol in portfolio:
        user['value'] += portfolio[symbol]['count'] * portfolio[symbol]['price']

    return render_template("index.html", portfolio=portfolio, user=user, usd=usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        quote = request.form.get("quote")
        shares = request.form.get("shares")

        if not quote.isalpha() or not shares.isdigit():
            return apology("need stock symbol and number of shares")

        quote = lookup(quote)
        print(quote)
        shares = int(shares)
        user = db.execute("SELECT * FROM users WHERE (id=:user_id)", user_id=session["user_id"])[0]

        if not quote:
            return apology("stock not found")
        if not user:
            return apology("user not found")
        if shares < 1:
            return apology("shares must be a positive number")
        if quote['price'] * shares > user['cash']:
            return apology("insufficent funds for purchase")

        stock = db.execute('SELECT * FROM stocks WHERE (symbol=:symbol)', symbol=quote['symbol'])
        if len(stock) < 1:
            db.execute('INSERT INTO stocks (name, symbol) VALUES (:name, :symbol)', name=quote['name'], symbol=quote['symbol'])
            stock = db.execute('SELECT * FROM stocks WHERE (symbol=:symbol)', symbol=quote['symbol'])
        stock = stock[0]

        db.execute('INSERT INTO transactions (user_id, stock_id, count, buy, price) VALUES (:user_id, :stock_id, :count, :buy, :price)', user_id=user['id'], stock_id=stock['id'], count=shares, buy=1, price=quote['price'])
        user['cash'] = user['cash'] - (quote['price'] * shares)
        db.execute('UPDATE users SET cash=:cash WHERE id=:user_id', cash=user['cash'], user_id=user['id'])

        return render_template("buy.html", shares=shares, quote=quote, usd=usd)

    return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    return apology("TODO")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quote = lookup(request.form.get("stock"))
        if not quote:
            return apology("stock not found")

        return render_template("quote.html", quote=quote, usd=usd)

    return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmed = request.form.get("confirm-password")

        if not username.isalnum() or not password.isalnum():
            return apology("username and password may only contain letters and numbers")

        if password != confirmed:
            return apology("passwords don't match")

        if db.execute("SELECT * FROM users WHERE username = :username", username=username):
            return apology("username is not available")

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username, password=pwd_context.hash(password))

        return render_template("index.html")
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user = db.execute("SELECT * FROM users WHERE (id=:user_id)", user_id=session["user_id"])[0]
    transactions = db.execute("SELECT * FROM transactions JOIN stocks ON transactions.stock_id = stocks.id WHERE transactions.user_id = :user_id", user_id=session["user_id"])
    portfolio = {}
    for tx in transactions:
        symbol = tx['symbol']
        if symbol in portfolio:
            if tx['buy'] == 1:
                portfolio[symbol]['count'] += tx['count']
            else:
                portfolio[symbol]['count'] -= tx['count']
        else:
            tx['price'] = lookup(symbol)['price']
            portfolio[symbol] = tx

    user['value'] = user['cash']
    for symbol in portfolio:
        user['value'] += portfolio[symbol]['count'] * portfolio[symbol]['price']

    if request.method == "POST":
        for name, value in request.form.items():
            value = int(value)
            if value > 0:
                data = name.split("_")
                db.execute('INSERT INTO transactions (user_id, stock_id, count, buy, price) VALUES (:user_id, :stock_id, :count, :buy, :price)', user_id=user['id'], stock_id=data[1], count=value, buy=0, price=data[0])
                cash = user['cash'] + float(data[0]) * value
                db.execute('UPDATE users SET cash=:cash WHERE id=:user_id', cash=cash, user_id=user['id'])


        return redirect(url_for("sell"))

    return render_template("sell.html", portfolio=portfolio, user=user, usd=usd)
