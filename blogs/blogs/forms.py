from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .models import User

class UserProfileForm(FlaskForm):
    email = StringField('Your Email:', validators=[DataRequired()])
    bio = TextAreaField('Your bio', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField('Your Email:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField('Log In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 80)])
    email = StringField('Your Email:', validators=[DataRequired(), Length(1, 120)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username_field):
        user = User.query.filter_by(username=username_field.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email_field):
        user = User.query.filter_by(email=email_field.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')
class AddPostForm(FlaskForm):
    post_name = StringField( validators=[DataRequired()]) 
    content = TextAreaField( validators = [DataRequired()])
