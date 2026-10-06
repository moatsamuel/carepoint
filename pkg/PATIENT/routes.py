from flask import render_template
from pkg.PATIENT import patient_bp

@patient_bp.route('/book')
def book():
    return render_template('patient/book_appt.html')