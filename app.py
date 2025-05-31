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
import os, db
from db import get_db_con
from models.user_model import User, get_user_by_id, get_user_by_email, update_password_for_email
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from config import Config
import threading

app = Flask(__name__)
app.config.from_object(Config)

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



app.register_blueprint(apartments_bp)
app.register_blueprint(tenants_bp)
app.register_blueprint(rental_agreements_bp)
app.register_blueprint(rent_payments_bp)
app.register_blueprint(dashboard_bp)

app.register_blueprint(auth_bp)

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
    allowed_endpoints = ['auth.login', 'auth.signup', 'static', 'index', 'reset_request', 'reset_token']
    
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
    return redirect(url_for("auth.login"))

@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if request.method == "POST":
        email = request.form.get("email")
        # Lookup user by email (assuming User model)
        user = get_user_by_email(email)
        if user:
            token = s.dumps(user.email, salt="password-reset-salt")
            link = url_for("reset_token", token=token, _external=True)
            try:
                send_reset_email(user.email, link)
                print("Email sent successfully")
            except Exception as e:
                print("⚠️ Email sending failed:", e)
        flash("If your email exists, a reset link has been sent.")
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html")

# def send_reset_email(to, link):
#     msg = Message("Password Reset Request", recipients=[to])
#     msg.body = f"""Hi there,
# To reset your password, visit the following link:
# {link}

# If you did not make this request, simply ignore this email.
# """
#     mail.send(msg)


def send_reset_email(to, link):
    print(f"🚨 MOCK EMAIL to: {to}")
    print(f"Reset link: {link}")


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


#@app.route('/logout')
#@login_required
#def logout():
    #logout_user()
    #return redirect('/login')

#if __name__ == '__main__':
 #   with app.app_context():
  #      db.create_all()
   # app.run(port=5007, debug=True)

#{# <a href="{{ url_for('reset_request') }}" class="forgot-password">Forgot password?</a> #}
