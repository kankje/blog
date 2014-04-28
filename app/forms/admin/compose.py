from flask.ext.wtf import Form
from wtforms import HiddenField, TextField, TextAreaField, SubmitField
from wtforms.validators import InputRequired


class ComposeForm(Form):
    id = HiddenField()
    title = TextField('Title', [InputRequired()])
    content = TextAreaField('Content', [InputRequired()])
    submit = SubmitField('Save')
