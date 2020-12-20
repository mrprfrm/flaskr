from flask_wtf import FlaskForm
from wtforms import validators
from wtforms import StringField
from wtforms.widgets import TextArea


class PostForm(FlaskForm):
    title = StringField(validators=[
        validators.InputRequired()
    ])
    body = StringField(widget=TextArea())
