from auth.decorators import login_required
from server.urls import lazy_url_for
from server.views import ListView, RetrieveView, CreateView, UpdateView, DeleteView

from .forms import PostForm, PostUpdateForm
from .models import Post


class PostListView(ListView):
    template_name = 'index.html'

    def get_collection(self):
        return Post.query.order_by(Post.created.desc())


class PostRetrieveView(RetrieveView):
    decorators = [login_required()]
    entity = Post
    template_name = 'retrieve.html'


class PostCreateView(CreateView):
    decorators = [login_required()]
    entity = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = lazy_url_for('blog.posts')


class PostUpdateView(UpdateView):
    decorators = [login_required()]
    entity = Post
    form_class = PostUpdateForm
    template_name = 'update.html'
    success_url = lazy_url_for('blog.posts')


class PostDeleteView(DeleteView):
    decorators = [login_required()]
    entity = Post
    success_url = lazy_url_for('blog.posts')
