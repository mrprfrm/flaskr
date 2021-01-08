from flask import g
from flask_wtf import FlaskForm
from wtforms import validators, ValidationError
from wtforms import StringField
from wtforms.widgets import TextArea

from blog.models import Post


class PostForm(FlaskForm):
    title = StringField(validators=[
        validators.InputRequired()
    ])
    body = StringField(widget=TextArea())

    def populate_obj(self, obj):
        super(PostForm, self).populate_obj(obj)
        obj.user = g.user

    def validate_title(self, field):
        post = Post.query.filter(Post.title == field.data).first()
        if post is not None:
            raise ValidationError(f'Post with title {field.data} already exists.')


class PostUpdateForm(FlaskForm):
    title = StringField(validators=[
        validators.InputRequired()
    ])
    body = StringField(widget=TextArea())
