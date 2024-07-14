from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User
from datetime import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class MatchForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateTimeField('Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    players = SelectMultipleField('Players', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Match')
    
class EditMatchForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateTimeField('Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    players = SelectMultipleField('Players', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update Match')
