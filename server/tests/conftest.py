import os

import pytest
import tempfile

from server import create_app


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    yield app

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
