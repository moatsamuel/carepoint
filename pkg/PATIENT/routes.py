from flask import render_template
from pkg.PATIENT import patient_bp
from pkg.decorators import role_required


@patient_bp.route('/patient/dashboard')
@role_required('PATIENT')
def dashboard():
    return render_template('patient/dashboard.html')

@patient_bp.route('/book')
@role_required('PATIENT')
def book():
    return render_template('patient/book_appt.html')