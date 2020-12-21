from flask import Blueprint, g, redirect, render_template, request, url_for

from auth import login_required
from db import db, get_object_or_404

from .forms import PostForm
from .models import Post

blueprint = Blueprint('blog', __name__)


@blueprint.route('/')
def index():
    posts = Post.query.order_by(Post.created.desc())
    return render_template('blog/index.html', posts=posts)


@blueprint.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post(title=form.title.data, body=form.body.data, user=g.user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.index'))
    return render_template('blog/create.html', form=form)


@blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_object_or_404(Post, Post.id==id)
    form = PostForm(request.form, obj=post)
    if request.method == 'POST' and form.validate():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        return redirect(url_for('blog.index'))
    return render_template('blog/update.html', form=form, post=post)


@blueprint.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_object_or_404(Post, Post.id==id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))
