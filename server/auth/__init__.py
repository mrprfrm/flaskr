import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from .forms import LoginForm, RegisterForm
from .models import User


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
        g.user = User.query.get(user_id)


@bluepirnt.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.username==form.username.data).first()
        if user is None:
            password_hash = generate_password_hash(form.password.data)
            user = User(username=form.username.data, password=password_hash)
            db.session.add(user)
            db.session.commit()
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(f'User with username {form.username.data} already exists.')
    return render_template('auth/register.html', form=form)


@bluepirnt.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.username==form.username.data).first()

        if user is not None and check_password_hash(user.password, form.password.data):
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash('Incorrect username and password combination.')
    return render_template('auth/login.html', form=form)


@bluepirnt.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
