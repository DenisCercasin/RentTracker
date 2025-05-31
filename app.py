from flask import Flask, render_template, session, redirect, url_for, request
from functools import wraps
from routes.auth import auth_bp
from routes.apartments import apartments_bp
from routes.tenants import tenants_bp
from flask_login import current_user, LoginManager, UserMixin
import os
from routes.rental_agreements import rental_agreements_bp
from routes.rent_payments import rent_payments_bp
from routes.dashboard import dashboard_bp
import os, db
from db import get_db_con
from models.user_model import User, get_user_by_id



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
    allowed_endpoints = ['auth.login', 'auth.signup', 'static', 'index']
    
    if request.endpoint in allowed_endpoints:
        return
    
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))  # redirect if not logged i

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


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
