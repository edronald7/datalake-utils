from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from ..forms import LoginForm
from ..models import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))