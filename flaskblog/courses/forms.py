from random import choices
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, IntegerField ,SelectField, SelectMultipleField, TextAreaField, HiddenField, FieldList, FormField, DateField
from wtforms.validators import DataRequired

class CourseFilterForm(FlaskForm):
    student = SelectField('Student', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Update')