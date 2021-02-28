import click
from flask import g, abort, current_app
from flask.cli import with_appcontext
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


def get_object_or_404(model, query=True):
    obj = model.query.filter(query).first()
    if obj:
        return obj
    abort(404, "Item doesn't exist.")


def get_db(e=None):
    if not 'db' in g:
        g.db = db


def close_db(e=None):
    global db
    db.session.remove()
    g.pop('db', None)


@click.command('init-db')
@with_appcontext
def init_db_command():
    global db
    import auth.models
    import blog.models
    db.create_all()
    click.echo('Initialized the database.')


def init_app(app):
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        app.before_request(get_db)
        app.teardown_appcontext(close_db)
        app.cli.add_command(init_db_command)
