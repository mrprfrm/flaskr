from flask_wtf import FlaskForm
from wtforms import validators
from wtforms import StringField, PasswordField


class LoginForm(FlaskForm):
    username = StringField(validators=[validators.InputRequired()])
    password = PasswordField(validators=[validators.InputRequired()])


class RegisterForm(FlaskForm):
    username = StringField(validators=[validators.InputRequired()])
    password = PasswordField(validators=[
        validators.InputRequired(),
        validators.EqualTo('confirm', message="Password and it's confirmation doesn't match" )
    ])
    confirm = PasswordField('Repeat password')
