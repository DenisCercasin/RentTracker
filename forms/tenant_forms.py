from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, ValidationError, StringField, FileField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from flask_wtf.file import FileAllowed
import re # Python-Bibliothek für reguläre Ausdrücke, wird für Passwortprüfung verwendet

# Funktion zur Definition einer benutzerdefinierten Passwortregel
def StrongPassword():
    def _strong_password(form, field): # Innere Funktion, die tatsächlich prüft, ob das Passwort stark genug ist
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
        InputRequired(), EqualTo("password", message="Passwords must match.")
    ])
    submit = SubmitField("Submit")

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'} # definieren der erlaubte Dateien 
class TenantForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=2)]) #Validators ist ein Argument 
    tel_num = StringField('Telephone Number', validators=[InputRequired()])
    document = FileField('Upload Document', validators=[
        FileAllowed(ALLOWED_EXTENSIONS, 'Unsupported file type.')
    ])
    submit = SubmitField('Submit')

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')
