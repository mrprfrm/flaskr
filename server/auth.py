import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db


bluepirnt = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapper(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapper


@bluepirnt.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        query = 'SELECT * FROM users WHERE id = ?'
        g.user = get_db().execute(query, (user_id,)).fetchone()


@bluepirnt.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None

        select_query = 'SELECT id FROM users WHERE username = ?'
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(select_query, (username,)).fetchone() is not None:
            error = f'User with username {username} already exists.'

        if error is None:
            query = 'INSERT INTO users (username, password) VALUES (?, ?)'
            password_hash = generate_password_hash(password)
            db.execute(query, (username, password_hash))
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)

    return render_template('auth/register.html')


@bluepirnt.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None

        query = 'SELECT * FROM users WHERE username = ?'
        user = db.execute(query, (username,)).fetchone()

        if user is None:
            error = 'Incorrect username.'
        if not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)

    return render_template('auth/login.html')


@bluepirnt.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
