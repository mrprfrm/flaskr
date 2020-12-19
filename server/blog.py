from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db


blueprint = Blueprint('blog', __name__)


def get_post(id):
    query = 'SELECT posts.id, title, body, created, author_id, username' \
            ' FROM posts JOIN users ON posts.author_id = users.id' \
            ' WHERE posts.id = ?'
    post = get_db().execute(query, (id,)).fetchone()

    if post is None:
        abort(404, f"Post with id {id} doesn't exist.")
    if post['author_id'] != g.user['id']:
        abort(403)

    return post

@blueprint.route('/')
def index():
    db = get_db()
    query = 'SELECT posts.id, title, body, created, author_id, username'\
            ' FROM posts JOIN users ON posts.author_id = users.id'\
            ' ORDER BY created DESC'
    posts = db.execute(query).fetchall()
    return render_template('blog/index.html', posts=posts)


@blueprint.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        error = None

        if not title:
            error = 'Title is required.'

        if error is None:
            db = get_db()
            query = 'INSERT INTO posts (title, body, author_id) VALUES (?, ?, ?)'
            db.execute(query, (title, body, g.user['id']))
            db.commit()
            return redirect(url_for('blog.index'))
        flash(error)

    return render_template('blog/create.html')


@blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        error = None

        if not title:
            error = 'Title is required.'

        if error is None:
            db = get_db()
            query = 'UPDATE posts SET title = ?, body = ? WHERE id = ?'
            db.execute(query, (title, body, id))
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@blueprint.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    query = 'DELETE FROM posts WHERE id = ?'
    db.execute(query, (id,))
    db.commit()
    return redirect(url_for('blog.index'))
