from flask import Blueprint, g, session

from .views import RegisterView, LoginView, logout
from .models import User


blueprint = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')
blueprint.add_url_rule('/register', view_func=RegisterView.as_view('register'))
blueprint.add_url_rule(rule='/login', view_func=LoginView.as_view('login'))
blueprint.add_url_rule('logout', view_func=logout)


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
