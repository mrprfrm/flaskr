import pytest

from blog.models import Post
from server.db import db


@pytest.fixture
@pytest.mark.usefixtures('app', 'user')
def post(app, user, faker):
    with app.app_context():
        _post = Post(
            title=faker.name(),
            body=faker.text(),
            user=user
        )

        db.session.add(_post)
        db.session.commit()
        return _post
