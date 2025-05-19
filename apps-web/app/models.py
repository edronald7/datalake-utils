from . import db
from flask_login import UserMixin
from . import login_manager

from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column('password', db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    nickname = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    cli_aws_profile = db.Column(db.String(250), unique=False, nullable=True)
    cli_aws_options = db.Column(db.String(250), unique=False, nullable=True)
    cli_oci_profile = db.Column(db.String(250), unique=False, nullable=True)
    cli_oci_options = db.Column(db.String(250), unique=False, nullable=True)
    

    @property
    def password(self):
        raise AttributeError('password is write-only')

    @password.setter
    def password(self, plaintext_password):
        self._password = generate_password_hash(plaintext_password)

    def verify_password(self, plaintext_password):
        return check_password_hash(self._password, plaintext_password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))