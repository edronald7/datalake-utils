from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app import create_app, db
from app.models import User
from config import Config

setup_bp = Blueprint('setup', __name__)

@setup_bp.route('/setup')
def admin():
    app = create_app()

    with app.app_context():
        db.create_all()
        go_home = "<a href='/'>Go to Home</a>"
        if not User.query.filter_by(username='admin').first():
            conf = Config()
            user = User(username='admin', is_admin=True)
            user.password = conf.DEFAULT_ADMIN_PASSWORD
            user.nickname = 'Admin App'
            db.session.add(user)
            db.session.commit()
            return f"✅ User 'admin' created successfully, with password \"{conf.DEFAULT_ADMIN_PASSWORD}\".<br> You can change the default password on file config.py. <br><br>{go_home}"

        else:
            return f"ℹ️ User 'admin' already exists. <br><br>{go_home}"