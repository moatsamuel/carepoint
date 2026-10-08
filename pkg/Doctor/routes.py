from flask import render_template, session, redirect, url_for, flash, abort
from pkg.models import Doctor, Appointment
from pkg.DOCTOR import doctor_bp


@doctor_bp.before_request
def doctor_only():
    if 'user_id' not in session:
        flash('Please log in to continue.', 'error')
        return redirect(url_for('auth.login'))
    if session.get('role') != 'DOCTOR':
        abort(403)


@doctor_bp.route('/dashboard')
def dashboard():
    doctor = Doctor.query.filter_by(user_id=session['user_id']).first()
    if doctor is None:
        abort(403)

    appointments = (
        Appointment.query
        .filter_by(doctor_id=doctor.id)
        .order_by(Appointment.appointment_date.asc(), Appointment.appointment_time.asc())
        .all()
    )
    return render_template('doctor/dashboard.html', doctor=doctor, appointments=appointments)