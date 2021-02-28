from flask import Blueprint

from blog.views import PostListView, PostRetrieveView, \
    PostCreateView, PostDeleteView, PostUpdateView


blueprint = Blueprint('blog', __name__, template_folder='templates')
blueprint.add_url_rule('/', view_func=PostListView.as_view('posts'))
blueprint.add_url_rule('/<int:pk>', view_func=PostRetrieveView.as_view('posts_retrieve'))
blueprint.add_url_rule('/create', view_func=PostCreateView.as_view('posts_create'))
blueprint.add_url_rule('/<int:pk>/update', view_func=PostUpdateView.as_view('posts_update'))
blueprint.add_url_rule('/<int:pk>/delete', view_func=PostDeleteView.as_view('posts_delete'))
