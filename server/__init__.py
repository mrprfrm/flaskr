import os

from flask import Flask

from .db import init_app
from .auth import bluepirnt


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='secret',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return 'Hello word!'

    db.init_app(app)
    app.register_blueprint(bluepirnt)

    return app
