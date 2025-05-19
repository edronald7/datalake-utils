import os

class Config:
    DEFAULT_ADMIN_PASSWORD = os.environ.get('DLU_ADMIN_PASSWORD') or 'admin'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key-please-change-this'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
