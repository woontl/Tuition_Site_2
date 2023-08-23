from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
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
    grade = SelectField('Grade', choices=['Grade 6','Grade 7','Grade 8','Grade 9','Grade 10','Grade 11','Grade 12'], validators=[DataRequired()])
    password = PasswordField('Password', 
                              validators=[DataRequired()]) #Must enter password
    confirm_password = PasswordField('Confirm Password',
                                    validators = [DataRequired(), #Must enter password
                                    EqualTo('password')]) #Both passwords must be equal
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
                        validators=[DataRequired()])
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
    grade = SelectField('Grade', choices=[6,7,8,9,10,11,12])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    
    submit = SubmitField('Update')

    def validate_username(self, username): #Perform validation checks only if new user/email is different from current user/email
        if current_user.account_type != 'Admin':
            if username.data != current_user.username:
                user = User.query.filter_by(username=username.data).first()
                if user:
                    raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email): #Perform validation checks only if new user/email is different from current user/email
        if current_user.account_type != 'Admin': 
            if email.data != current_user.email:
                user = User.query.filter_by(email=email.data).first()
                if user:
                    raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), #Must enter email
                        Email()]) #Checks if email is legit
    submit = SubmitField('Send')
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
    submit = SubmitField('Reset')

    
class ContactForm(FlaskForm):
    name = StringField('Name', 
                            validators=[DataRequired(), #Must enter a name
                            Length(min=2, max=20)]) #name must be between 2-20 characters
    age = StringField('Age', 
                            validators=[DataRequired(),
                            Length(min=1, max=2)]) 
    number = StringField('Number', 
                            validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), #Must enter email
                        Email()]) #Checks if email is legit
    school = StringField('School', 
                        validators=[DataRequired()]) 
    grade = SelectField('Grade', choices=['Grade 6','Grade 7','Grade 8','Grade 9','Grade 10','Grade 11','Grade 12'], validators=[DataRequired()])
    syllabus = StringField('Syllabus', 
                    validators=[DataRequired()]) 
    enquiry = TextAreaField('Enquiry', validators=[DataRequired()])
    submit = SubmitField('Send')