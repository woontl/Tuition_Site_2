from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired
    
class ChangelogForm(FlaskForm):
    version = StringField('Version', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post')
    
class BugForm(FlaskForm):
    issue = StringField('Issue', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices = ['Open','In Progress','Closed'], validators=[DataRequired()])

    submit = SubmitField('Post')