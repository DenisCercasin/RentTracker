from flask import Flask, render_template
from flask_mail import Mail
from routes.apartments import apartments_bp
from routes.tenants import tenants_bp
from routes.login import login_bp
from routes.signup import signup_bp
from flask_sqlalchemy import SQLAlchemy
import os,db


app = Flask(__name__)
db1 = SQLAlchemy(app)
mail = Mail(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SECRET_KEY'] = '619619'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail-Konfiguration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rent.tracker.hwr@gmail.com'  # E-Mail-Adresse korrekt
app.config['MAIL_PASSWORD'] = ''  # App-spezifisches Passwort von Google

app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    DATABASE=os.path.join(app.instance_path, 'rent_tracker.sqlite')
)


class User(UserMixin, db.Model):
    id = db1.Column(db1.Integer, primary_key=True)
    name = db1.Column(db1.String(200), nullable=False)
    email = db1.Column(db1.String(200), unique=True, nullable=False)
    password = db1.Column(db1.String(200), nullable=False)

    def get_token(self, expires_sec=3600):
        token_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return token_serializer.dumps({'user_id': self.id})

    @staticmethod
    def verify_token(token, expires_sec=3600):
        token_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            user_id = token_serializer.loads(token, max_age=expires_sec)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)
    
app.cli.add_command(db.init_db)
app.teardown_appcontext(db.close_db_con)



app.register_blueprint(apartments_bp)
app.register_blueprint(tenants_bp)
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)


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