from auth.decorators import login_required
from urls import lazy_url_for
from views import ListView, RetrieveView, CreateView, UpdateView, DeleteView

from .forms import PostForm, PostUpdateForm
from .models import Post


class PostListView(ListView):
    template_name = 'blog/index.html'

    def get_collection(self):
        return Post.query.order_by(Post.created.desc())


class PostRetrieveView(RetrieveView):
    decorators = [login_required()]
    entity = Post
    template_name = 'blog/retrieve.html'


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
    template_name = 'blog/update.html'
    success_url = lazy_url_for('blog.posts')


class PostDeleteView(DeleteView):
    decorators = [login_required()]
    entity = Post
    success_url = lazy_url_for('blog.posts')
