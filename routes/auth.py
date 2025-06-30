from flask import Blueprint, request, redirect, render_template, session, url_for, flash, current_app
from db.db import get_db_con
from services.utils import is_strong_password
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from models.user import User
from forms.tenant_forms import LoginForm, SignupForm
from db.sqlalchemy_base import alchemy
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from itsdangerous import URLSafeTimedSerializer
import os


auth_bp = Blueprint("auth", __name__) #Flask-Blueprints für Authentifizierungsrouten

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        conn = get_db_con()
        existing = User.query.filter_by(email=email).first()# Prüfen, ob ein Benutzer mit dieser E-Mail bereits existiert     
        if existing:
            flash ("User already exists.", "warning")
            return render_template("auth/signup.html", form = form, error="User already exists.")

        user = User(name=name, email=email)  # Neuen Benutzer erstellen
        user.set_password(password)

        alchemy.session.add(user)# Benutzer zur Datenbank hinzufügen
        alchemy.session.commit()

        #login_user(user)  # Benutzer einloggen

        #flash("Account created succesfully, enjoy.", "success")
        #return redirect(url_for("dashboard.index", show_guide="true"))
        
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        token = s.dumps(user.email, salt="email-confirm-salt")
        confirm_link = url_for("auth.confirm_email", token=token, _external=True)

        try:
            send_confirmation_email(user.email, confirm_link)
        except Exception as e:
            print("⚠️ Email sending failed:", e)

        return redirect(url_for("auth.signup_requested"))
    
    return render_template("auth/signup.html", form = form)

@auth_bp.route("/signup_requested")
def signup_requested():
    return render_template("auth/signup_requested.html")

 # Wenn GET-Anfrage oder Formular ungültig: Registrierungsformular anzeigen
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        conn = get_db_con()
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return render_template("auth/login.html", form = form, error="Invalid credentials.")
        
        login_user(user)
        return redirect(url_for("dashboard.index"))#wenn gültig, dann Weiterleitung zum Dashboard
    
    return render_template("auth/login.html", form = form)#Wenn ungültig, Weiterleitung zum Login

@auth_bp.route("/confirm/<token>")
def confirm_email(token):
    try:
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        email = s.loads(token, salt="email-confirm-salt", max_age=86400)
    except Exception as e:
        flash("Confirmation link is invalid or has expired.", "danger")
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Account not found.", "warning")
        return redirect(url_for("auth.login"))

    login_user(user)

    flash("Email confirmed. You are now logged in.", "success")
    return redirect(url_for("dashboard.index", show_guide="true"))

def send_confirmation_email(to_email, link):
    message = Mail(
        from_email='rent.tracker.hwr@gmail.com',
        to_emails=to_email,
        subject='Confirm Your RentTracker Account',
        html_content=f"""
         <p>Hello,</p>
        <p>Thanks for signing up for Rent Tracker!</p>
        <p>To activate your account, please confirm your email by clicking the link below:</p>
        <p><a href="{link}">{link}</a></p>
        <p>This link will expire in 24 hours.</p>
        <p>Best regards,<br>The Rent Tracker Team</p>
        <hr>
        <p>If you didn’t sign up for Rent Tracker, you can ignore this email.</p>
        """
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        #sg.set_sendgrid_data_residency("eu")
        response = sg.send(message)
        print(f"Email sent: {response.status_code}")
    except Exception as e:
        print("Email sending failed:", e)