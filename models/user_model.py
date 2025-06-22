from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_base import alchemy

class User(alchemy.Model, UserMixin):
    __tablename__ = "user"

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    name = alchemy.Column(alchemy.String, nullable=False)
    email = alchemy.Column(alchemy.String, unique=True, nullable=False)
    password = alchemy.Column(alchemy.String, nullable=False)
    reminder_day = alchemy.Column(alchemy.Integer, nullable=True)
    reminder_enabled = alchemy.Column(alchemy.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        print("was set")

    def check_password(self, password):
        return check_password_hash(self.password, password)

@staticmethod
def update_password_for_email(email, new_password):
    user = User.query.filter_by(email=email).first()
    if user:
        user.set_password(new_password)
        alchemy.session.commit()