import re
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_mail import Message, Mail
from itsdangerous import URLSafeTimedSerializer
from app import db1, mail

def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[a-z]", password) and
        re.search(r"[A-Z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )


    
def send_mail(user):
    token = user.get_token()
    reset_url = url_for('reset_with_token', token=token, _external=True)
    msg = Message(
        subject='Password Reset Request',
        recipients=['carenkedis1@gmail.com'],
        sender='deniscercasin@gmail.com',
        body=f'''To reset your password, click the following link:
                {reset_url}
                If you did not request this, please ignore this email.
                ''')
    mail.send(msg)