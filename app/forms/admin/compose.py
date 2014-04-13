from wtforms import HiddenField, TextField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Regexp

from lib.web import Form


class ComposeForm(Form):
    id = HiddenField()
    title = TextField('Title', [InputRequired()])
    content = TextAreaField('Content', [InputRequired()])
    submit = SubmitField('Save')
