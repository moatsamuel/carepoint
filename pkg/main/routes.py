from flask import render_template
from pkg import db
# from pkg.models import Specialty, Doctor
from pkg.main import main_bp
# from pkg.decorators import role_required

@main_bp.route('/')
def landing():
    return render_template('care_landing.html')



@main_bp.app_errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403


@main_bp.app_errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404


