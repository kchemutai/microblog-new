from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Required, ValidationError
from microblog.models import User
from flask_login import current_user
from flask_wtf.file import FileAllowed, FileField


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           Required(), Length(min=5, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValueError(
                'That email is already taken, please choose another')

    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if username:
            raise ValueError(
                'That username is already taken, please choose another')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
                           Required(), Length(min=5, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValueError(
                    'That email is already taken, please choose another')

    def validate_username(self, username):
        if username.data != current_user.username:
            username = User.query.filter_by(username=username.data).first()
            if username:
                raise ValueError(
                    'That username is already taken, please choose another')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class PasswordResetRequestForm(FlaskForm):

    email = StringField('Reset Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValueError(
                'That email is not Valid, Please use a valid email')


class PasswordResetForm(FlaskForm):

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')
