import os

from flask import Flask

from db import init_app
from auth import bluepirnt as auth_blueprint
from blog import blueprint as blog_blueprint


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    db_path = os.path.join(app.instance_path, 'flaskr.sqlite')
    app.config.from_mapping(
        SECRET_KEY='secret',
        DATABASE=db_path,
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=True
    )
    #
    if config is not None:
        app.config.from_mapping(config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_app(app)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(blog_blueprint)
    app.add_url_rule('/', endpoint='index')

    return app
