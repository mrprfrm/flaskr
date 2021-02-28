from flask import session, flash, render_template, redirect, url_for, g
from werkzeug.security import generate_password_hash, check_password_hash

from server.urls import lazy_url_for
from server.views import FormView

from .forms import RegisterForm, LoginForm
from .models import User


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = lazy_url_for('blog.posts')

    def perform_post(self, form, **kwargs):
        password_hash = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=password_hash)
        g.db.session.add(user)
        g.db.session.commit()
        session.clear()
        session['user_id'] = user.id


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = lazy_url_for('blog.posts')

    def perform_post(self, form, **kwargs):
        user = User.query.filter(User.username == form.username.data).first()
        if user is None or not check_password_hash(user.password, form.password.data):
            flash('Incorrect username and password combination.')
            return render_template(self.template_name, form=form)
        session.clear()
        session['user_id'] = user.id


def logout():
    session.clear()
    return redirect(url_for('blog.posts'))
