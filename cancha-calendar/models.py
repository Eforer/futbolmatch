from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cancha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    reservations = db.relationship('Reservation', backref='cancha', lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    cancha_id = db.Column(db.Integer, db.ForeignKey('cancha.id'), nullable=False)
