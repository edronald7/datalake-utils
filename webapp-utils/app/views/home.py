from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    # Cath error: sqlalchemy.exc.OperationalError : sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
    try:
        # Check if the database is initialized
        from app import db
        from app.models import User
        db.session.query(User).first()
    except Exception as e:
        # If the database is not initialized, redirect to setup
        flash("Database not initialized. Please run setup.py.", "error")
        return redirect(url_for('setup.admin'))
    # Check if the user is authenticated


    # if autenticated, redirect to dashboard else show login page
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    else:
        return redirect(url_for('auth.login'))