from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, ValidationError, StringField
from wtforms.validators import InputRequired, Email, Length, EqualTo
import re

def StrongPassword():
    def _strong_password(form, field):
        password = field.data
        if len(password) < 5:
            raise ValidationError("Password must be at least 5 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must include at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must include at least one lowercase letter.")
        if not re.search(r"\d", password):
            raise ValidationError("Password must include at least one number.")
        if not re.search(r"\W", password):
            raise ValidationError("Password must include at least one special character.")
    return _strong_password

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), StrongPassword()])
    submit = SubmitField("Submit")

class SignupForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=2)])
    email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), StrongPassword()])
    confirm = PasswordField("Confirm Password", validators=[
        InputRequired(), EqualTo(password, message="Passwords must match.")
    ])
    submit = SubmitField("Submit")


