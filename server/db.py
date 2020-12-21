import click
from flask import g, abort
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def get_object_or_404(model, query=True):
    obj = model.query.filter(query).first()
    if obj:
        return obj
    abort(404, "Item doesn't exist.")


def close_db(e=None):
    global db
    db.session.remove()
    g.pop('alchemy', None)


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
        global db
        db.init_app(app)
        app.teardown_appcontext(close_db)
        app.cli.add_command(init_db_command)
        g.db = db
