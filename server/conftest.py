import os

import pytest
import tempfile

from server.db import db
from server import create_app
from auth.models import User


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SERVER_NAME': 'server'
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
@pytest.mark.usefixtures('app')
def client(app):
    return app.test_client()


@pytest.fixture
@pytest.mark.usefixtures('app')
def runner(app):
    app.test_cli_runner()


@pytest.fixture
@pytest.mark.usefixtures('app', 'faker')
def user(app, faker):
    with app.app_context():
        _user = User(
            username=faker.user_name(),
            password=faker.password()
        )

        db.session.add(_user)
        db.session.commit()
        return _user
