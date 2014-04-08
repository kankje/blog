from wtforms import TextField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

from lib.web import Form


class InstallForm(Form):
    username = TextField('Username', [
        InputRequired(),
        Length(3, 200)
    ])
    password = PasswordField('Password', [
        InputRequired(),
        Length(6, 200)
    ])
    password_confirm = PasswordField('Confirm password', [
        InputRequired(),
        Length(6, 200),
        EqualTo('password', "The passwords don't match.")
    ])
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
