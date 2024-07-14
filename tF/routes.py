import requests
from flask import render_template, url_for, flash, redirect, request, session
from app import app, db, bcrypt
from forms import RegistrationForm, LoginForm, MatchForm, EditMatchForm
from models import User, Match, user_match
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    try:
        matches = Match.query.all()
        if not matches:
            flash('No matches found.', 'warning')
        return render_template('match_list.html', matches=matches)
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
        return render_template('match_list.html', matches=[])

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/match/join/<int:match_id>")
@login_required
def join_match(match_id):
    match = Match.query.get_or_404(match_id)
    if match.players.count() < 10:
        match.players.append(current_user)
        db.session.commit()
        flash('You have joined the match!', 'success')
    else:
        flash('This match is already full.', 'danger')
    return redirect(url_for('home'))

@app.route("/match/cancel/<int:match_id>", methods=['POST'])
@login_required
def cancel_match(match_id):
    match = Match.query.get_or_404(match_id)
    if match.organizer != current_user:
        flash('You do not have permission to cancel this match.', 'danger')
        return redirect(url_for('home'))
    db.session.delete(match)
    db.session.commit()
    flash('The match has been canceled.', 'success')
    return redirect(url_for('home'))

@app.route('/check_availability', methods=['GET', 'POST'])
def check_availability():
    if request.method == 'POST':
        cancha_id = request.form.get('cancha_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not cancha_id or not start_date or not end_date:
            error_message = "Missing required parameters"
            return render_template('check_availability.html', error_message=error_message)

        response = requests.get('http://localhost:5000/api/availability', params={
            'cancha_id': cancha_id,
            'start_date': start_date,
            'end_date': end_date
        })

        if response.status_code == 400:
            error_message = response.json().get("error")
            return render_template('check_availability.html', error_message=error_message)

        availability = response.json()
        return render_template('availability.html', availability=availability)

    return render_template('check_availability.html')

@app.route("/match/edit/<int:match_id>", methods=['GET', 'POST'])
@login_required
def edit_match(match_id):
    match = Match.query.get_or_404(match_id)
    if match.organizer != current_user:
        flash('You do not have permission to edit this match.', 'danger')
        return redirect(url_for('home'))
    
    form = MatchForm()
    form.players.choices = [(user.id, user.username) for user in User.query.all()]
    
    if form.validate_on_submit():
        match.title = form.title.data
        match.date = form.date.data
        match.location = form.location.data
        
        selected_players = form.players.data
        match.players = [User.query.get(player_id) for player_id in selected_players if User.query.get(player_id)]
        
        db.session.commit()
        flash('The match has been updated.', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = match.title
        form.date.data = match.date
        form.location.data = match.location
        form.players.data = [player.id for player in match.players]
    
    return render_template('edit_match.html', title='Edit Match', form=form, match=match)

@app.route("/match/new", methods=['GET', 'POST'])
@login_required
def new_match():
    form = MatchForm()
    form.players.choices = [(user.id, user.username) for user in User.query.all()]
    
    if request.method == 'POST':
        match = Match(
            title=form.title.data,
            date=form.date.data,
            location=form.location.data,
            organizer=current_user
        )
        db.session.add(match)
        db.session.commit()
        
        session['match_id'] = match.id
        flash('Match created. Now add players to the match.', 'success')
        return redirect(url_for('add_players'))
    
    return render_template('create_match.html', title='Crear Partido', form=form)

@app.route("/match/add_players", methods=['GET', 'POST'])
@login_required
def add_players():
    match_id = session.get('match_id')
    if not match_id:
        flash('No match found in session. Please create a match first.', 'danger')
        return redirect(url_for('new_match'))
    
    match = Match.query.get(match_id)
    form = MatchForm()
    form.players.choices = [(user.id, user.username) for user in User.query.all() if user not in match.players]
    
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user = User.query.get_or_404(user_id)
        if user not in match.players:
            match.players.append(user)
            db.session.commit()
            flash(f'{user.username} added to the match.', 'success')
        else:
            flash(f'{user.username} is already in the match.', 'warning')
        return redirect(url_for('add_players'))
    
    return render_template('add_players.html', title='Agregar Jugadores', form=form, match=match)

@app.route("/match/finish_creation", methods=['GET', 'POST'])
@login_required
def finish_creation():
    match_id = session.pop('match_id', None)
    if not match_id:
        flash('No match found in session. Please create a match first.', 'danger')
        return redirect(url_for('new_match'))
    
    flash('Match creation completed.', 'success')
    return redirect(url_for('home'))

@app.route("/match/remove_player/<int:match_id>/<int:user_id>", methods=['POST'])
@login_required
def remove_player(match_id, user_id):
    match = Match.query.get_or_404(match_id)
    user = User.query.get_or_404(user_id)
    if match.organizer != current_user:
        flash('You do not have permission to edit this match.', 'danger')
        return redirect(url_for('home'))
    if user in match.players:
        match.players.remove(user)
        db.session.commit()
        flash(f'{user.username} removed from the match.', 'success')
    else:
        flash(f'{user.username} is not in the match.', 'warning')
    return redirect(url_for('edit_match', match_id=match_id))
