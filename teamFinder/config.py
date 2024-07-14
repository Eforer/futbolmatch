import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/futbol_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'password'
    MYSQL_DB = 'futbol_app'
