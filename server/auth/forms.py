from flask_wtf import FlaskForm
from wtforms import validators, ValidationError
from wtforms import StringField, PasswordField

from auth.models import User


class LoginForm(FlaskForm):
    username = StringField(validators=[validators.InputRequired()])
    password = PasswordField(validators=[validators.InputRequired()])


class RegisterForm(FlaskForm):
    username = StringField(validators=[validators.InputRequired()])
    password = PasswordField(validators=[
        validators.InputRequired(),
        validators.EqualTo('confirm', message="Password and it's confirmation doesn't match")
    ])
    confirm = PasswordField('Repeat password')

    def validate_username(self, field):
        user = User.query.filter(User.username == field.data).first()
        if user is not None:
            raise ValidationError(f'User with username {field.data} already exists.')
