import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/futbol_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
