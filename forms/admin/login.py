from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

from lib.web import Form


class LoginForm(Form):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired(), Length(-1, 200)])
    submit = SubmitField('Login')
