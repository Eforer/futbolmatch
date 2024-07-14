from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime, timedelta
from database import db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tu_usuario:tu_contraseña@localhost/tu_base_de_datos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, nullable=False)
    
@app.route('/', methods=['GET'])
def show_login_form():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session['logged_in'] = True
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Credenciales incorrectas. Inténtalo de nuevo.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('show_login_form'))

@app.route('/home')
def home():
    if 'logged_in' in session and session['logged_in']:
        user_id = session.get('user_id')
        friend_ids = [f.friend_id for f in Friendship.query.filter_by(user_id=user_id).all()]

        if not friend_ids:
            no_friends_message = "No tienes amigos agregados aún."
            users = User.query.filter(User.id != user_id).all()
            return render_template('home.html', no_friends_message=no_friends_message, users_data=users)
        else:
            friendships_data = User.query.filter(User.id.in_(friend_ids)).all()
            users = User.query.filter(User.id != user_id, ~User.id.in_(friend_ids)).all()
            return render_template('home.html', users_data=users, friendships_data=friendships_data)
    else:
        return redirect(url_for('show_login_form'))

@app.route('/delete/<int:id>')
def delete(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    user = User.query.get(id)
    if user:
        user.nombre = request.form['nombre']
        user.apellido = request.form['apellido']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/user', methods=['POST'])
def add_user():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    password = request.form['password']
    fecha_nacimiento = datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date()

    edad_minima = timedelta(days=16*365)
    fecha_limite = datetime.now().date() - edad_minima
    if fecha_nacimiento > fecha_limite:
        flash("Debes tener al menos 16 años para registrarte.", "error")
        return redirect(url_for('home'))

    if len(password) < 8:
        flash("La contraseña debe tener al menos 8 caracteres.", "error")
        return redirect(url_for('home'))

    if nombre and apellido and email and password:
        new_user = User(nombre=nombre, apellido=apellido, email=email, password=password, fecha_nacimiento=fecha_nacimiento)
        db.session.add(new_user)
        db.session.commit()
        flash("Usuario registrado exitosamente.", "success")
    return redirect(url_for('home'))

@app.route('/add_friend/<int:friend_id>', methods=['POST'])
def add_friend(friend_id):
    if 'user_id' not in session:
        return redirect(url_for('show_login_form'))

    user_id = session['user_id']
    new_friendship = Friendship(user_id=user_id, friend_id=friend_id)
    db.session.add(new_friendship)
    db.session.commit()

    reciprocal_friendship = Friendship(user_id=friend_id, friend_id=user_id)
    db.session.add(reciprocal_friendship)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/view_profile/<int:friend_id>', methods=['GET'])
def view_profile(friend_id):
    friend = User.query.get(friend_id)

    if friend:
        return render_template('profile.html', friend_data=friend)
    else:
        return "Usuario no encontrado", 404

@app.route('/delete_friend/<int:friend_id>')
def delete_friend(friend_id):
    user_id = session['user_id']
    friendship = Friendship.query.filter_by(user_id=user_id, friend_id=friend_id).first()
    if friendship:
        db.session.delete(friendship)
        db.session.commit()

    reciprocal_friendship = Friendship.query.filter_by(user_id=friend_id, friend_id=user_id).first()
    if reciprocal_friendship:
        db.session.delete(reciprocal_friendship)
        db.session.commit()

    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)
