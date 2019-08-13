import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, make_response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required


app = Flask(__name__)
db = SQL("sqlite:///bak.db")
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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/book", methods=["POST", "GET"])
@login_required
def book():
    if request.method == "POST":
        name = request.form.get("name")
        menu_id = int(request.form.get("menu_id"))

        check = db.execute("SELECT * FROM menu_list WHERE id=:id_given", id_given=menu_id)
        if check == []:
            return render_template("error.html", message="NO ITEMS AVALIABLE  ")

        rate = check[0]["rate"]
        db.execute("INSERT INTO order_list (user_id,order_for,menu_id,rate) VALUES (:user_id,:order_for,:menu_id,:rate)",
                   user_id=session["user_id"], order_for=name, menu_id=menu_id, rate=rate)
        return render_template("success.html")
    else:
        menu_list = db.execute("SELECT * FROM menu_list")
        return render_template("index.html", menu_list=menu_list)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message='user name required')

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message='Password required')

        # Query database for username
        rows = db.execute("SELECT * FROM new_user WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", message='Invalid user name or Password')

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("Logged In")

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if (request.method == "POST"):

        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return render_template("error.html", message='Fill the form')

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if (password != confirmation):
            return render_template("error.html", message='Password did not match')

        checkusername = db.execute("SELECT username FROM new_user WHERE username = :username", username=username)

        if (checkusername != []):
            return render_template("error.html", message='User Name Not available')

        hashed = generate_password_hash(password)
        new_user = db.execute("INSERT INTO new_user (username,hash) VALUES (:username,:hashed)", username=username, hashed=hashed)

        session["user_id"] = new_user

        flash("Registered!")

        return redirect("/")

    else:
        return render_template("register.html")
