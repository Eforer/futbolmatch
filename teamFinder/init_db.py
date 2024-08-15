from app import app, db, bcrypt
from models import User, Match

with app.app_context():
    # Elimina todas las tablas
    db.drop_all()
    
    # Crea todas las tablas
    db.create_all()

    # Insertar usuarios de ejemplo con contraseñas hasheadas
    users = [
        User(username='user1', email='user1@example.com', password=bcrypt.generate_password_hash('password1').decode('utf-8')),
        User(username='user2', email='user2@example.com', password=bcrypt.generate_password_hash('password2').decode('utf-8')),
        User(username='user3', email='user3@example.com', password=bcrypt.generate_password_hash('password3').decode('utf-8')),
        User(username='user4', email='user4@example.com', password=bcrypt.generate_password_hash('password4').decode('utf-8')),
        User(username='user5', email='user5@example.com', password=bcrypt.generate_password_hash('password5').decode('utf-8')),
        User(username='user6', email='user6@example.com', password=bcrypt.generate_password_hash('password6').decode('utf-8')),
        User(username='user7', email='user7@example.com', password=bcrypt.generate_password_hash('password7').decode('utf-8')),
        User(username='user8', email='user8@example.com', password=bcrypt.generate_password_hash('password8').decode('utf-8')),
        User(username='user9', email='user9@example.com', password=bcrypt.generate_password_hash('password9').decode('utf-8')),
    ]

    for user in users:
        db.session.add(user)

    db.session.commit()

    # Insertar partido de ejemplo
    match = Match(title='Partido Amistoso', date='2024-07-01 18:00:00', location='Cancha Central', organizer_id=1)
    db.session.add(match)
    db.session.commit()

    # Asociar usuarios al partido
    match.players.extend(users[:5])
    db.session.commit()
