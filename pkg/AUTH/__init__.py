from flask import Blueprint

auth_bp = Blueprint("auth",__name__)

from pkg.AUTH import routes