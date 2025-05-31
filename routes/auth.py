from flask import Blueprint, request, redirect, render_template, session, url_for, flash
from db import get_db_con
from logic import is_strong_password
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from models.user_model import User


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if not is_strong_password(password):
            return render_template("signup.html", error="Weak password.")

        conn = get_db_con()
        existing = conn.execute("SELECT id FROM user WHERE email = ?", (email,)).fetchone()
        if existing:
            return render_template("signup.html", error="User already exists.")

        hashed_pw = generate_password_hash(password)
        conn.execute("INSERT INTO user (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_pw))
        conn.commit()
        flash("Account created. Please log in.")
        return redirect(url_for("auth.login"))
    return render_template("signup.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_con()
        user_row = conn.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()
        if not user_row or not check_password_hash(user_row["password"], password):
            return render_template("login.html", error="Invalid credentials.")
        
        user = User(user_row["id"], user_row["name"], user_row["email"])

        login_user(user)
        return redirect(url_for("dashboard.index"))
    else:
        return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
