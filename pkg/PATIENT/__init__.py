from flask import Blueprint

patient_bp = Blueprint('patient', __name__)

from pkg.PATIENT import routes