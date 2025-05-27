from flask import Blueprint, request, render_template, redirect
from app import db1, User # need to be adjusted - now 2 db, one for sqlite connection and 1 for sqlalchemy
from logic import is_strong_password

signup_bp = Blueprint ("signup", __name__)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def get_signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not is_strong_password(password):
            error = "Password must be at least 8 characters and include uppercase, lowercase, number, and a symbol."
            return render_template('signup.html', error=error)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            error = "User already exists!"
            return render_template('signup.html', error=error)

        user = User(name=name, email=email, password=password)
        db1.session.add(user)
        db1.session.commit()
        return redirect('/login') # maybe later to adjust not to login but directly  to overview

    return render_template('signup.html')