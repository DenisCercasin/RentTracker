from flask import Blueprint, request, redirect, render_template, session, url_for, flash
from db import get_db_con
from logic.logic import is_strong_password
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from models.user_model import User
from forms import LoginForm, SignupForm
from sqlalchemy_base import alchemy

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        conn = get_db_con()
        existing = User.query.filter_by(email=email).first()        
        if existing:
            flash ("User already exists.", "warning")
            return render_template("signup.html", form = form, error="User already exists.")

        user = User(name=name, email=email)
        user.set_password(password)

        alchemy.session.add(user)
        alchemy.session.commit()

        flash("Account created. Please log in.")
        return redirect(url_for("dashboard.index", show_guide="true"))
    
    return render_template("signup.html", form = form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        conn = get_db_con()
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return render_template("login.html", form = form, error="Invalid credentials.")
        
        login_user(user)
        return redirect(url_for("dashboard.index"))
    
    return render_template("login.html", form = form)

