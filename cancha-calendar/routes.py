from flask import render_template, redirect, url_for, flash, jsonify, request
from app import app
from models import Cancha, Reservation, db
from forms import ReservationForm
from datetime import datetime, time, timedelta

@app.route('/')
def index():
    view_type = request.args.get('view_type', 'week')
    selected_date = request.args.get('selected_date', datetime.now().date().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()

    if view_type == 'day':
        start_date = selected_date
        end_date = selected_date
    elif view_type == 'week':
        start_date = selected_date - timedelta(days=selected_date.weekday())
        end_date = start_date + timedelta(days=6)
    else:  # month view
        start_date = selected_date.replace(day=1)
        end_date = (start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1)) if start_date.month < 12 else datetime(selected_date.year + 1, 1, 1) - timedelta(days=1)

    reservations = Reservation.query.filter(Reservation.date >= start_date, Reservation.date <= end_date).all()
    dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    canchas = Cancha.query.all()

    reservations_by_date = {}
    for reservation in reservations:
        if reservation.date not in reservations_by_date:
            reservations_by_date[reservation.date] = {}
        if reservation.cancha_id not in reservations_by_date[reservation.date]:
            reservations_by_date[reservation.date][reservation.cancha_id] = {}
        reservations_by_date[reservation.date][reservation.cancha_id][reservation.start_time] = reservation

    return render_template('index.html', canchas=canchas, dates=dates, view_type=view_type, selected_date=selected_date, reservations_by_date=reservations_by_date, time=time)

@app.route('/reserve/<int:cancha_id>/<date>/<time>', methods=['GET', 'POST'])
def reserve(cancha_id, date, time):
    form = ReservationForm()
    if form.validate_on_submit():
        reservation = Reservation(
            date=datetime.strptime(date, '%Y-%m-%d').date(),
            start_time=datetime.strptime(time, '%H:%M').time(),
            end_time=(datetime.strptime(time, '%H:%M') + timedelta(hours=1)).time(),
            user_name=form.user_name.data,
            cancha_id=cancha_id
        )
        db.session.add(reservation)
        db.session.commit()
        flash('Reserva realizada con éxito', 'success')
        return redirect(url_for('index'))
    return render_template('reserve.html', form=form)

@app.route('/delete_reservation/<int:reservation_id>', methods=['POST'])
def delete_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if reservation:
        db.session.delete(reservation)
        db.session.commit()
        flash('Reserva eliminada con éxito', 'success')
    else:
        flash('Reserva no encontrada', 'danger')
    return redirect(url_for('index'))

import logging

logging.basicConfig(level=logging.DEBUG)

@app.route('/api/availability', methods=['GET'])
def get_availability():
    cancha_id = request.args.get('cancha_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    app.logger.debug(f'Received request with cancha_id={cancha_id}, start_date={start_date}, end_date={end_date}')

    if not cancha_id or not start_date or not end_date:
        app.logger.error('Missing required parameters')
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        app.logger.error('Invalid date format')
        return jsonify({"error": "Invalid date format"}), 400

    reservations = Reservation.query.filter(
        Reservation.cancha_id == cancha_id,
        Reservation.date >= start_date,
        Reservation.date <= end_date
    ).all()

    availability = []
    for reservation in reservations:
        availability.append({
            'date': reservation.date.strftime('%Y-%m-%d'),
            'start_time': reservation.start_time.strftime('%H:%M'),
            'end_time': reservation.end_time.strftime('%H:%M'),
            'user_name': reservation.user_name
        })

    app.logger.debug(f'Returning availability: {availability}')
    return jsonify(availability)