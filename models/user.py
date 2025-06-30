from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from db.sqlalchemy_base import alchemy

class User(alchemy.Model, UserMixin):
    __tablename__ = "user" # Name der Tabelle in der Datenbank

    id = alchemy.Column(alchemy.Integer, primary_key=True) # Primärschlüssel (eindeutig)
    name = alchemy.Column(alchemy.String, nullable=False) #Name darf nicht leer sein
    email = alchemy.Column(alchemy.String, unique=True, nullable=False)
    password = alchemy.Column(alchemy.String, nullable=False)
    reminder_day = alchemy.Column(alchemy.Integer, nullable=True)
    reminder_enabled = alchemy.Column(alchemy.Boolean, default=False)
    is_confirmed = alchemy.Column(alchemy.Boolean, default=False)

 # Methode zum sicheren Speichern eines Passworts (mit Hashing)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password) # Vergleich: eingegebenes Passwort vs. gespeichertes Hash


@staticmethod #wenn Userpass vergisst 
def update_password_for_email(email, new_password):
    user = User.query.filter_by(email=email).first()#Abfrage auf die User-Tabelle
    if user:
        user.set_password(new_password)
        alchemy.session.commit() #speichern