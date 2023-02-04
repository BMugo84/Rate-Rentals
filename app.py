
import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import valid_password, login_required, scam_catcher
import requests
from PIL import Image
import io


# Configur application
app = Flask(__name__)

# Ensure templates are autoreloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# configure sessions to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 library to use SQLite database *** to be added once i decide on the name
db = SQL("sqlite:///rentals.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register User"""

    # Register user
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check pass
        if not username or not email or not password or not confirmation:
            flash("Please check if you have filled all values")
        elif password != confirmation:
            flash("Your passwords don't match")
        elif not valid_password(password):
            flash("Password must contain letters, numbers and special characters for strength")

        # Check if username exists
        rows = db.execute("SELECT username FROM users WHERE username = ?", username)
        if len(rows) > 0:
            flash("Username already exists")

        # All checks passed. Push to database
        db.execute("INSERT INTO users (username, email, password) VALUES(?, ?, ?) ", username, email, generate_password_hash(password))

    # Render the template
    return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("invalid username and/or password")

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

# Now we start the real stuff
@app.route("/")
@login_required
def index():
    # Display rental properties
    rows = db.execute("SELECT rentals.*, COUNT(ratings.id) as rating_count, (SELECT COUNT(*) FROM comments WHERE comments.rentals_id = rentals.id) as comment_count FROM rentals LEFT JOIN ratings ON rentals.id = ratings.rentals_id GROUP BY rentals.id")

    #display maps, pushpins in index with focused location box

    bing_maps_key = "AsSfaPbdQ-0wjDXPkIJyNtmGG0FpQelb35hCBTRmZqJf_g3T2kR7SfwdMvvAd8Cj"
    return render_template('index.html', rows=rows, bing_maps_key=bing_maps_key)

# Add rentals
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        name = request.form.get("name")
        rooms = request.form.get("rooms")
        rent = request.form.get("rent")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        description = request.form.get("description")

        # Convert rooms and rent to int. apparently forms returns stringformat only
        rooms = int(rooms)
        rent = int(rent)

        # Check validity
        if not name or not rooms or not rent or not description:
            flash("Please fill out all the fields")
        elif rooms < 1:
            flash("rooms can't be less than 1")
        elif not isinstance(rooms, int) and not (isinstance(rooms, float) and rooms.is_integer()):
            flash("Number of rooms must be a number")
        elif not isinstance(rent, int) and not (isinstance(rent, float) and rent.is_integer()):
            flash("Rent must be a number")

        db.execute("INSERT INTO rentals ( name, rooms, rent, description) VALUES(?, ?, ?, ?)", name, rooms, rent, description )
        return redirect('/')

    return render_template('add.html')

# single post in an array of posts
@app.route("/index/<int:rentals_id>", methods=["GET", "POST"])
def comments(rentals_id):
    rentals = db.execute("SELECT * FROM rentals WHERE id = ?", rentals_id)
    comments = db.execute("SELECT * FROM comments WHERE rentals_id = ?", rentals_id)
    ratings = db.execute("SELECT AVG(landlord_strictness), AVG(quality), AVG(size), AVG(security), AVG(rent) FROM ratings WHERE rentals_id = ?", rentals_id)
    bing_maps_key = "AsSfaPbdQ-0wjDXPkIJyNtmGG0FpQelb35hCBTRmZqJf_g3T2kR7SfwdMvvAd8Cj"
    return render_template('comments.html', rentals=rentals, comments=comments, ratings=ratings, bing_maps_key=bing_maps_key)

# Decided to add_comment function that requires a login auth instead of a user requiring to sign in to view comments
@app.route("/add_comment/<int:rentals_id>", methods=["GET", "POST"])
@login_required
def add_comment(rentals_id):
    if request.method == "POST":
        comment = request.form.get("comment")

        # Check if post is empty
        if not comment:
            flash("please comment something")
        elif scam_catcher(comment):
            flash("No phone numbers allowed on comments")

        db.execute("INSERT INTO comments (rentals_id, user_id, comment, time) VALUES(?, ?, ?, datetime('now'))", rentals_id, session["user_id"], comment)
    return redirect(url_for('comments', rentals_id=rentals_id))

# Adding ratings system
@app.route("/rate/<int:rentals_id>", methods=["GET", "POST"])
@login_required
def rate(rentals_id):
    rentals = db.execute("SELECT * FROM rentals WHERE id = ?", rentals_id)
    if request.method == "POST":
        try:
            landlord_strictness = int(request.form.get("landlord_strictness"))
            quality = int(request.form.get("quality"))
            size = int(request.form.get("size"))
            security = int(request.form.get("security"))
            rent = int(request.form.get("rent"))
        except ValueError:
            flash("Invalid input")

        if not landlord_strictness or not quality or not size or not security or not rent:
            flash("All inputs required")

        db.execute("INSERT INTO ratings (user_id, rentals_id, landlord_strictness, quality, size, security, rent) VALUES(?, ?, ?, ?, ?, ?, ?)", session["user_id"], rentals_id, landlord_strictness, quality, size, security, rent)
        return redirect("/")
    return render_template('rate.html', rentals=rentals)
