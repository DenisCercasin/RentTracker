from flask import Flask, render_template, session, redirect, url_for, request, flash
from functools import wraps
from routes.auth import auth_bp
from routes.apartments import apartments_bp
from routes.tenants import tenants_bp
from flask_login import current_user, LoginManager, UserMixin, logout_user
import os
from routes.rental_agreements import rental_agreements_bp
from routes.rent_payments import rent_payments_bp
from routes.dashboard import dashboard_bp
from routes.settings import settings_bp
from routes.reminders_api import reminders_api_bp
import os, db
from db import get_db_con
from models.user_model import User, get_user_by_id, get_user_by_email, update_password_for_email
from itsdangerous import URLSafeTimedSerializer
#from config import Config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    DATABASE=os.path.join(app.instance_path, 'rent_tracker.sqlite')
)

app.cli.add_command(db.init_db)
app.teardown_appcontext(db.close_db_con)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # or your correct login route name
login_manager.init_app(app)

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

load_dotenv()

app.register_blueprint(apartments_bp)
app.register_blueprint(tenants_bp)
app.register_blueprint(rental_agreements_bp)
app.register_blueprint(rent_payments_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(reminders_api_bp)

@app.route("/")
def index():
    return render_template("landing_page.html")

@app.route("/insert/sample")
def run_insert_sample():
    db.insert_sample()
    return "Database flushed and populated with more sample data"

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper

@app.before_request
def require_login():
    allowed_endpoints = ['auth.login', 'auth.signup', 'static', 'index', 'reset_request', 'reset_token', 'run_insert_sample']
    
    if request.endpoint in allowed_endpoints:
        return
    
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))  # redirect if not logged in

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("landing_page.html")

@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if request.method == "POST":
        email = request.form.get("email")
        # Lookup user by email
        user = get_user_by_email(email)
        if user:
            token = s.dumps(user.email, salt="password-reset-salt")
            link = url_for("reset_token", token=token, _external=True)
            try:
                send_reset_email(user.email, link)
            except Exception as e:
                print("⚠️ Email sending failed:", e)
        else:
            print("No user with this email.")
        flash("If your email exists, a reset link has been sent.")
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html")


# def send_reset_email(to, link):
#     print(f"🚨 MOCK EMAIL to: {to}")
#     print(f"Reset link: {link}")

def send_reset_email(to_email, link):
    message = Mail(
        from_email='rent.tracker.hwr@gmail.com',
        to_emails=to_email,
        subject='Reset Your RentTracker Password',
        html_content=f"""
        <p>Hello,</p>
        <p>You requested a password reset for your RentTracker account.</p>
        <p>Click the link below to reset your password:</p>
        <p><a href="{link}">{link}</a></p>
        <p>This link will expire in 1 hour.</p>
        <hr>
        <p>If you didn’t request this, you can ignore this email.</p>
        """
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        #sg.set_sendgrid_data_residency("eu")
        response = sg.send(message)
        print(f"✅ Email sent: {response.status_code}")
    except Exception as e:
        print("❌ Email sending failed:", e)

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    try:
        email = s.loads(token, salt="password-reset-salt", max_age=3600)  # 1 hour
    except:
        flash("The reset link is invalid or has expired.", "danger")
        return redirect(url_for("reset_request"))

    if request.method == "POST":
        new_password = request.form.get("password")
        update_password_for_email(email, new_password)
        flash("Your password has been updated. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_token.html")


