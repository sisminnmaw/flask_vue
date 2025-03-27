from flask import Blueprint

bp = Blueprint('frontend', __name__)

from app.api.frontend import routes 