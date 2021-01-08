import functools

from flask import g, redirect, url_for, request


def login_required(methods=('GET', 'POST', 'PUT', 'PATCH', 'DELETE')):
    def decorator(view):
        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            if g.user is None and request.method in methods:
                return redirect(url_for('auth.login'))
            return view(*args, **kwargs)
        return wrapper
    return decorator
