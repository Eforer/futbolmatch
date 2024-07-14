import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask_user:flask_password@localhost/fb_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
