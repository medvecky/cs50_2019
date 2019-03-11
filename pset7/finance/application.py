import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, make_response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, password_check

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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # get user portfolio info from data base

    stocks = db.execute(
        "SELECT * FROM portfolio WHERE userid = :userid",
        userid=session["user_id"])
    totalStocksPrice = 0
    for stock in stocks:
        totalStocksPrice += round((round(float(stock["price"]), 2) * int(stock["numberofshares"])), 2)
    userBalance = round(float(db.execute(
        "SELECT cash FROM users WHERE id = :userid",
        userid=session["user_id"])[0]["cash"]), 2)
    grandBalance = round(userBalance, 2) + round(totalStocksPrice, 2)
    return render_template(
        "index.html",
        stocks=stocks,
        userBalance="${:,.2f}".format(userBalance),
        grandBalance="${:,.2f}".format(grandBalance))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # validate form inputs
        if not request.form.get("symbol"):
            return apology("symbols missing", 403)
        elif not request.form.get("shares"):
            return apology("shares missing", 403)
        else:
            # validate shares
            try:
                numberOfShares = int(request.form.get("shares"))
            except Exception:
                return apology("invalid shares count", 400)
            if numberOfShares < 0:
                return apology("invalid shares count", 400)
            # get quote by symbol
            quote = lookup(request.form.get("symbol"))
            # validate received data
            if not quote:
                return apology("invalid symbol", 400)
            # get total price
            totalPrice = quote["price"] * int(request.form.get("shares"))
            # get user balance
            userBalance = float(db.execute(
                "SELECT cash FROM users WHERE id=:userId",
                userId=session["user_id"])[0]["cash"])
            # validate user balance
            if totalPrice > userBalance:
                return apology("Can't afford", 400)
            # check is stock exist in users partfolio
             # add stocks to portfolio
            result = db.execute(
                "SELECT * FROM portfolio WHERE userid=:userid and symbol=:symbol",
                userid=session["user_id"],
                symbol=quote["symbol"])
            if not result:
                # add stocks to portfolio
                result = db.execute(
                    "INSERT INTO portfolio (userid,symbol,name,price,numberofshares) VALUES (:userid,:symbol,:name,:price,:numberofshares)",
                    userid=session["user_id"],
                    symbol=quote["symbol"],
                    name=quote["name"],
                    price=float(quote["price"]),
                    numberofshares=int(request.form.get("shares")))
                # check status of user insertion
                if not result:
                    return apology("Error when insert into partfolio", 400)
            else:
                # update existed stock info
                result = db.execute(
                    "UPDATE portfolio SET numberofshares=numberofshares + :numberofshares WHERE userid=:userid and symbol=:symbol",
                    numberofshares=int(request.form.get("shares")),
                    userid=session["user_id"],
                    symbol=quote["symbol"])
                # check status of user update
                if not result:
                    return apology("Error when update partfolio", 400)
            # update history
            result = db.execute(
                "INSERT INTO history (userid, symbol, numberofshares, price) VALUES (:userid, :symbol, :numberofshares, :price)",
                userid=session["user_id"],
                symbol=quote["symbol"],
                numberofshares=int(request.form.get("shares")),
                price=float(quote["price"]))
            if not result:
                return apology("failed update history", 400)
            # update users cash balance
            result = db.execute(
                "UPDATE users SET cash = cash - :totalPrice WHERE id = :userId",
                totalPrice=totalPrice,
                userId=session["user_id"])
            if not result:
                return apology("failed update user cash balance", 400)
            flash("Bought!")
            return redirect("/")

    else:
        value = request.args.get("symbol")
        if not value:
            return render_template("buy.html")
        return render_template("buy.html", value=value)


@app.route("/history")
@login_required
def history():
    # just return history page
    result = db.execute("SELECT * FROM history WHERE userid = :userid", userid=session["user_id"])
    if not result:
        return apology("fail to get history data", 400)
    return render_template("history.html", items=result)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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


# render rpofile operation option page
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


# Add cash page handler
@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def addCash():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # check amount for existence
        if not request.form.get("amount"):
            return apology("amount missing", 403)
        else:
            # validate amount
            try:
                amount = round(float(request.form.get("amount")), 2)
            except Exception:
                return apology("Invalid amount value", 400)
            if amount < 0:
                return apology("Invalid amount value", 400)
        # update amount in database and resdirect
        result = db.execute(
            "UPDATE users SET cash = cash + :amount WHERE id = :userid",
            amount=amount,
            userid=session["user_id"])
        if not result:
            return apology("failed to update cash")
        flash(usd(amount) + " added to balance")
        return redirect("/")
    else:
        return render_template("add_cash.html")


# change pasword page
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def changePassword():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # validate input fields
        if not request.form.get("old_password"):
            return apology("old password missing", 400)
        elif not request.form.get("new_password"):
            return apology("new password missing", 400)
        elif not request.form.get("confirmation"):
            return apology("confirmation missing", 400)
        else:
            # Query database for current password
            rows = db.execute(
                "SELECT * FROM users WHERE id = :userid",
                userid=session["user_id"])
            # validate password for correctnew
            if not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
                return apology("old password not match", 403)
            elif request.form.get("new_password") != request.form.get("confirmation"):
                return apology("new password and comfirmation must match", 403)
            elif request.form.get("new_password") == request.form.get("old_password"):
                return apology("new password same as old", 403)
            elif password_check(request.form.get("new_password")) == False:
                return apology("new password too weak")
            else:
                # update password in database
                passwordHash = generate_password_hash(request.form.get("new_password"))
                result = db.execute(
                    "UPDATE users SET hash = :passwordHash WHERE id = :userid",
                    passwordHash=passwordHash,
                    userid=session["user_id"])
                flash("Password changed!")
                return redirect("/")
    else:
        return render_template("change_password.html")


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
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # validate form input
        if not request.form.get("symbol"):
            return apology("Missing symbol", 400)
        else:
            # get data from service API
            quote = lookup(request.form.get("symbol"))
            # validate received data
            if not quote:
                return apology("invalid symbol", 400)
            else:
                # output stock data
                return render_template("quote_data.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
         # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Ensure password and confirmation match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("password and confirmation must match", 400)
        # Check password quality
        elif password_check(request.form.get("password")) == False:
            return apology("password is too weak", 400)

        # generate hash for entered password
        passwordHash = generate_password_hash(request.form.get("password"))

        # try to add user to db
        result = db.execute(
            "INSERT INTO users (username, hash) VALUES (:username, :passwordHash)",
            username=request.form.get("username"),
            passwordHash=passwordHash)

        # check status of user insertion
        if not result:
            return apology("User already exist")

         # Query database for id
        rows = db.execute(
            "SELECT * FROM users WHERE username = :username",
            username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # validate form inputs
        if not request.form.get("symbol"):
            return apology("symbols missing", 403)
        elif not request.form.get("shares"):
            return apology("shares missing", 403)
        else:
            # get quote by symbol
            quote = lookup(request.form.get("symbol"))
            # validate received data
            if not quote:
                return apology("invalid symbol", 400)
            # get and validate available share
            availableShares = int(db.execute(
                "SELECT numberofshares FROM portfolio WHERE userid = :userid and symbol = :symbol",
                userid=session["user_id"],
                symbol=quote["symbol"])[0]["numberofshares"])
            if availableShares < int(request.form.get("shares")):
                return apology("too many shares", 400)
            # get total price
            totalPrice = quote["price"] * int(request.form.get("shares"))
            # update parfolio info
            # if not all shares sold
            if availableShares - int(request.form.get("shares")) > 0:
                result = db.execute(
                    "UPDATE portfolio SET numberofshares = numberofshares - :sold WHERE userid = :userid and symbol = :symbol",
                    sold=request.form.get("shares"),
                    userid=session["user_id"],
                    symbol=request.form.get("symbol"))
                if not result:
                    return apology("portfolio update failed", 400)
            # if all shares sold
            else:
                result = db.execute(
                    "DELETE FROM portfolio WHERE userid = :userid and symbol = :symbol",
                    userid=session["user_id"],
                    symbol=request.form.get("symbol"))
                if not result:
                    return apology("failed delete from portfolio")
            # update history
            result = db.execute(
                "INSERT INTO history (userid, symbol, numberofshares, price) VALUES (:userid, :symbol, :numberofshares, :price)",
                userid=session["user_id"],
                symbol=quote["symbol"],
                numberofshares=-int(request.form.get("shares")),
                price=float(quote["price"]))
            if not result:
                return apology("failed update history", 400)
            # update user balance
            result = db.execute(
                "UPDATE users SET cash = cash + :totalprice where id = :userid",
                totalprice=totalPrice,
                userid=session["user_id"])
            if not result:
                apology("failed to update users info", 400)
            # go to index page
            flash("Sold!")
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        value = request.args.get("symbol")
        if not value:
            # get stocks symbols from user's partfolio
            results = db.execute(
                "SELECT symbol FROM portfolio WHERE userid = :userid",
                userid=session["user_id"])
            symbols = []
            for result in results:
                symbols.append(result["symbol"])
            # render template with only existed inpartfolio stocks
            return render_template("sell.html", symbols=symbols)
        return render_template("sell.html", value=value)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
