from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ReservationForm(FlaskForm):
    user_name = StringField('Nombre del solicitante', validators=[DataRequired()])
    submit = SubmitField('Reservar')
