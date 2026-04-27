from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
recipe_bp = Blueprint('recipe', __name__)

from . import auth_routes
from . import recipe_routes
