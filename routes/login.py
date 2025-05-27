from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, LoginManager, login_required, current_user
from app import User

login_bp = Blueprint ("login", __name__)

#login_manager = LoginManager()
#login_manager.login_view = 'get_login'
#login_manager.init_app(app)


@login_bp.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user is None:
            return "❌ User not found."
        if user.password != password:
            return "❌ Incorrect password."

        login_user(user)
        return redirect('/overview') #url_for()

    return render_template('login.html')

"""@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            print("hi")
            send_mail(user)
            print("hi2")
            return "Reset-Link wurde an deine E-Mail gesendet."
        else:
            error = "Email address not found."
            return render_template('reset_password.html', error=error)
    return render_template('reset_password.html')
"""
"""@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    user = User.verify_token(token)
    if not user:
        return "Invalid or expired token."

    if request.method == 'POST':
        new_password = request.form['password']
        if not is_strong_password(new_password):
            return "Password must be at least 8 characters and include uppercase, lowercase, number, and symbol."
        user.password = new_password
        db.session.commit()
        return redirect('/login')

    return render_template('reset_with_token.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token. Please try again.', 'warning')
        return redirect(url_for('reset_request'))

    if request.method == 'POST':
        new_password = request.form['password']
        if not is_strong_password(new_password):
            flash('Password not strong enough.', 'danger')
            return render_template('reset_with_token.html', token=token)

        user.password = new_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('get_login'))

    return render_template('reset_with_token.html', token=token)
"""
@login_bp.route('/overview')
@login_required
def dashboard():
    #base.html , user = curent_user
    #return render_template('overview.html')
    return render_template('base.html', user=current_user) #need to be replaced to overview_html

#@login_manager.user_loader
#def load_user(user_id):
    #return User.query.get(int(user_id))