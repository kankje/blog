from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo


class UserSettingsForm(Form):
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

    submit = SubmitField('Save')
