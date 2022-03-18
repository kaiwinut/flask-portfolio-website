from server import db
from server.models import User
from server.config import INVITATION
from hashlib import sha256
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in!', category='success')
                return redirect(url_for('blogpage.blog'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        invitation = request.form.get('invitation')

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(email=username).first()
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Passwords do not match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash('Email is invalid.', category='error')
        elif len(invitation) > 0 and not check_password_hash(INVITATION, invitation):
            flash('Invitation code is invalid', category='error')
        else:
            if len(invitation) > 0 and check_password_hash(INVITATION, invitation):
                new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'), invited=True)
            else:
                new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'), invited=False)

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!', category='success')
            return redirect(url_for('blogpage.blog'))

    return render_template('signup.html', user=current_user)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blogpage.blog'))