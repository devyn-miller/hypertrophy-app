from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required
from ..models import User
from .. import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(email=request.form['email'], name=request.form['name'])
        new_user.set_password(request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')
