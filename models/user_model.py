from flask_login import UserMixin
from db import get_db_con

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
