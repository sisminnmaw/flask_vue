from flask import Blueprint

bp = Blueprint('services', __name__)

from app.api.services import routes 