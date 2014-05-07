from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length


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
    custom_html = TextAreaField('Custom HTML')

    submit = SubmitField('Save')
