from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length

from lib.web import Form


class SettingsForm(Form):
    # TODO password fields
    blog_name = TextField('Blog name', [
        InputRequired(),
        Length(1, 200)
    ])
    blog_description = TextAreaField('Blog description', [
        InputRequired()
    ])
    blog_author = TextField('Blog author', [
        InputRequired(),
        Length(1, 200)
    ])
    submit = SubmitField('Save')
