from random import choices
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, IntegerField ,SelectField, SelectMultipleField, TextAreaField, HiddenField, FieldList, FormField, DateField
from wtforms.validators import DataRequired

class HomeworkForm(FlaskForm):
    title = StringField('Title')
    student = SelectField('Student', coerce=str, validators=[DataRequired()])
    deadline = DateField('Deadline', validators=[DataRequired()])
    topics = SelectField('Topics', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Post')

class QuestionForm(FlaskForm):
    title = StringField('Title')
    grade = SelectField('Grade', choices = ['ALL','IGCSE & O-Levels', 'IB & A-Levels'], validators=[DataRequired()])
    topics = SelectField('Topics', coerce=str, validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices = ['ALL','Easy','Moderate','Hard','Extreme'], validators=[DataRequired()])
    load_questions = SubmitField('Load Questions')
    submit = SubmitField('Post')

class QuestionBankForm(FlaskForm):
    grade = SelectField('Grade', choices = ['IGCSE & O-Levels', 'IB & A-Levels'], validators=[DataRequired()])
    topics = SelectMultipleField('Topics', coerce=str, validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices = ['Easy','Moderate','Hard','Extreme'], validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])
    img = FileField('Click to Upload Question Image', validators=[FileRequired(), FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Post')

class WorkingForm(FlaskForm):
    workings = HiddenField('Workings', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    submit = SubmitField('Check Answer')

class HomeworkFilterForm(FlaskForm):
    student = SelectField('Student', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Post')
    