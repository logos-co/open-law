# flake8: noqa F401
from .auth import auth_blueprint
from .main import main_blueprint
from .user import bp as user_blueprint
from .book import bp as book_blueprint
from .home import bp as home_blueprint
from .section import bp as section_blueprint
from .vote import bp as vote_blueprint
from .approve import bp as approve_blueprint
from .star import bp as star_blueprint
from .permission import bp as permissions_blueprint
