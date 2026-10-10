from flask import render_template, session, redirect, url_for, flash, abort
from pkg import db
from pkg.models import Doctor, Appointment
from pkg.DOCTOR import doctor_bp


@doctor_bp.before_request
def doctor_only():
    if 'user_id' not in session:
        flash('Please log in to continue.', 'error')
        return redirect(url_for('auth.login'))
    if session.get('role') != 'DOCTOR':
        abort(403)


def current_doctor():
    doctor = Doctor.query.filter_by(user_id=session['user_id']).first()
    if doctor is None:
        abort(403)
    return doctor


@doctor_bp.route('/dashboard')
def dashboard():
    doctor = current_doctor()
    appointments = (
        Appointment.query
        .filter_by(doctor_id=doctor.id)
        .order_by(Appointment.appointment_date.asc(), Appointment.appointment_time.asc())
        .all()
    )
    return render_template('doctor/dashboard.html', doctor=doctor, appointments=appointments)


# action name: (status it must be in now, status it becomes)
ALLOWED_CHANGES = {
    'accept':   ('Pending',  'Accepted'),
    'reject':   ('Pending',  'Rejected'),
    'complete': ('Accepted', 'Completed'),
}


@doctor_bp.route('/appointments/<int:appointment_id>/<action>', methods=['POST'])
def update_appointment(appointment_id, action):
    doctor = current_doctor()

    if action not in ALLOWED_CHANGES:
        abort(404)
    required_status, new_status = ALLOWED_CHANGES[action]

    # filtering by doctor_id is the ownership check
    appointment = Appointment.query.filter_by(
        id=appointment_id, doctor_id=doctor.id
    ).first_or_404()

    if appointment.status != required_status:
        flash(f'This appointment is {appointment.status.lower()} and cannot be changed that way.', 'error')
        return redirect(url_for('doctor.dashboard'))

    appointment.status = new_status
    db.session.commit()

    flash(f'Appointment marked as {new_status.lower()}.', 'success')
    return redirect(url_for('doctor.dashboard'))