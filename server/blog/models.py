import datetime

from server.db import db
from auth.models import User


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    body = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(User, backref='posts', lazy=True)
