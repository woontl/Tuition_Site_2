from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), #Must enter a name
                            Length(min=2, max=20)]) #name must be between 2-20 characters
    email = StringField('Email',
                        validators=[DataRequired(), #Must enter email
                        Email()]) #Checks if email is legit
    grade = SelectField('Grade', choices=[6,7,8,9,10,11,12,'Admin'],validators=[DataRequired()])
    password = PasswordField('Password', 
                              validators=[DataRequired()]) #Must enter password
    confirm_password = PasswordField('Confirm Password',
                                    validators = [DataRequired(), #Must enter password
                                    EqualTo('password')]) #Both passwords must be equal
    account_type = SelectField('Account Type', choices=['User','Admin'], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username): #Check if user is already in DB
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email): #Check if email is already in DB
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), #Must enter email
                        Email()]) #Checks if email is legit
    password = PasswordField('Password', 
                              validators=[DataRequired()]) #Must enter password
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), #Must enter a name
                            Length(min=2, max=20)]) #name must be between 2-20 characters
    email = StringField('Email',
                        validators=[DataRequired(), #Must enter email
                        Email()]) #Checks if email is legit
    grade = SelectField('Grade', choices=[6,7,8,9,10,11,12,'Admin'])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username): #Perform validation checks only if new user/email is different from current user/email
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email): #Perform validation checks only if new user/email is different from current user/email
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), #Must enter email
                        Email()]) #Checks if email is legit
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email): 
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email.')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', 
                              validators=[DataRequired()]) #Must enter password
    confirm_password = PasswordField('Confirm Password',
                                    validators = [DataRequired(), #Must enter password
                                    EqualTo('password')]) #Both passwords must be equal
    submit = SubmitField('Reset Password')
    
class UserDateForm(FlaskForm):
    description1 = StringField('Description 1', validators=[DataRequired()]) 
    date1 = DateField('Date 1', validators=[DataRequired()], format='%Y-%m-%d')
    time1 = TimeField('Time 1', validators=[DataRequired()], format='%H:%M')
    description2 = StringField('Description 2', validators=[DataRequired()]) 
    date2 = DateField('Date 2', validators=[DataRequired()], format='%Y-%m-%d')
    time2 = TimeField('Time 2', validators=[DataRequired()], format='%H:%M')
    description3 = StringField('Description 3', validators=[DataRequired()]) 
    date3 = DateField('Date 3', validators=[DataRequired()], format='%Y-%m-%d')
    time3 = TimeField('Time 3', validators=[DataRequired()], format='%H:%M')
    description4 = StringField('Description 4', validators=[DataRequired()]) 
    date4 = DateField('Date 4', validators=[DataRequired()], format='%Y-%m-%d')
    time4 = TimeField('Time 4', validators=[DataRequired()], format='%H:%M')
    submit = SubmitField('Update')
    
class UserTopicsForm(FlaskForm):
    topics = StringField('Topics', validators=[DataRequired()])
    checkbox = BooleanField('Completed?') 
    submit = SubmitField('Update')