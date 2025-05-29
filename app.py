from flask import Flask, render_template
from routes.auth import auth_bp
from routes.apartments import apartments_bp
from routes.tenants import tenants_bp
from routes.login import login_bp
from routes.signup import signup_bp
import os

from routes.rental_agreements import rental_agreements_bp
from routes.rent_payments import rent_payments_bp
from routes.dashboard import dashboard_bp
import os,db

app = Flask(__name__)

app.cli.add_command(db.init_db)
app.teardown_appcontext(db.close_db_con)



app.register_blueprint(apartments_bp)
app.register_blueprint(tenants_bp)
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)

app.register_blueprint(rental_agreements_bp)
app.register_blueprint(rent_payments_bp)
app.register_blueprint(dashboard_bp)

@app.route("/")
def index():
    return render_template("landing_page.html")

@app.route("/insert/sample")
def run_insert_sample():
    db.insert_sample()
    return "Database flushed and populated with more sample data"







#@app.route('/logout')
#@login_required
#def logout():
    #logout_user()
    #return redirect('/login')

#if __name__ == '__main__':
 #   with app.app_context():
  #      db.create_all()
   # app.run(port=5007, debug=True)
