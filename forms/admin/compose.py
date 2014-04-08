from wtforms import HiddenField, TextField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Regexp

from lib.web import Form


class ComposeForm(Form):
    id = HiddenField()
    title = TextField('Title', [InputRequired()])
    link_text = TextField('Link text', [
        InputRequired(),
        Regexp(r'[a-zA-Z0-9-]+', 0, 'Must only contain a-z, A-Z, 0-9 and dashes.')
    ])
    content = TextAreaField('Content', [InputRequired()])
    submit = SubmitField('Save')
