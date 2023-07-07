from random import choices
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, IntegerField ,SelectField, SelectMultipleField, TextAreaField, HiddenField, FieldList, FormField, DateField
from wtforms.validators import DataRequired

class LessonFilterForm(FlaskForm):
    student = SelectField('Student', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Post')

class LessonForm(FlaskForm):
    title = StringField('Title')
    student = SelectField('Student', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Post')

class LessonNotesForm(FlaskForm):
    workings = HiddenField('Workings')
    notes = TextAreaField('Summary Notes')
    formulas = TextAreaField('Formulas')
    topics = SelectField('Topics', coerce=str)
    workings = HiddenField('Workings')
    submit = SubmitField('Post')