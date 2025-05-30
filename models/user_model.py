from flask_login import UserMixin
from db import get_db_con
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

def get_user_by_id(user_id):
    conn = get_db_con()
    user_row = conn.execute("SELECT id, name, email FROM user WHERE id = ?", (user_id,)).fetchone()
    if user_row:
        return User(user_row["id"], user_row["name"], user_row["email"])
    return None

def get_user_by_email(email):
    conn = get_db_con()
    user_row = conn.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()
    if user_row:
        return User(user_row["id"], user_row["name"], user_row["email"])
    return None

def update_password_for_email(email, new_password):
    conn = get_db_con()
    hashed_pw = generate_password_hash(new_password)
    conn.execute("UPDATE user SET password = ? WHERE email = ?", (hashed_pw, email))
    conn.commit()
    conn.close()