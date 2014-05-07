from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import InputRequired


class ComposeForm(Form):
    title = TextField('Title', [InputRequired()])
    content = TextAreaField('Content', [InputRequired()])
    submit = SubmitField('Save')
