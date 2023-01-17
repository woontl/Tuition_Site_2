from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, FloatField
from wtforms.validators import DataRequired
    
class ChangelogForm(FlaskForm):
    version = StringField('Version', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Post')