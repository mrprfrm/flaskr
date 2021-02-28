from flask import url_for


def lazy_url_for(name):
    yield url_for(name)
