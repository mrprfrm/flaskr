import pytest
from flask import url_for


@pytest.mark.usefixtures('app', 'client', 'post')
def test_list(app, client):
    with app.app_context():
        url = url_for('blog.posts')
        response = client.get(url)
        assert response.status_code == 200
