from random import choices
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, TimeField ,SelectField, DateField
from wtforms.validators import DataRequired

class ExamsForm(FlaskForm):
    student = SelectField('Student', coerce=str)
    description1 = StringField('Description 1') 
    date1 = DateField('Date 1', format='%Y-%m-%d')
    description2 = StringField('Description 2') 
    date2 = DateField('Date 2', format='%Y-%m-%d')
    description3 = StringField('Description 3') 
    date3 = DateField('Date 3', format='%Y-%m-%d')
    submit = SubmitField('Update')