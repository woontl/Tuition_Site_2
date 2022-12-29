from flask_wtf import FlaskForm
from wtforms import SubmitField ,SelectField, StringField, HiddenField
from wtforms.validators import DataRequired

class NotesFilterForm(FlaskForm):
    student = SelectField('Student', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Post')
    
class NoteForm(FlaskForm):
    title = StringField('Title')
    student = SelectField('Student', coerce=str, validators=[DataRequired()])
    workings = HiddenField('Workings')
    submit = SubmitField('Post')