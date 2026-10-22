from flask import render_template , request, redirect, url_for, flash, session, abort
from pkg import db
from datetime import datetime, date
from pkg.models import Doctor, Patient, Appointment
from pkg.PATIENT import patient_bp
from pkg.decorators import role_required


def current_patient():
    patient = Patient.query.filter_by(user_id=session['user_id']).first()

    if patient is None:
        abort(403)

    return patient


@patient_bp.route('/patient/dashboard')
@role_required('PATIENT')
def dashboard():
    patient = current_patient()
    appointments = (
        Appointment.query
        .filter_by(patient_id=patient.id)
        .order_by(Appointment.appointment_date.asc(), Appointment.appointment_time.asc())
        .all()
    )
    return render_template('patient/dashboard.html', patient=patient, appointments=appointments)


@patient_bp.route('/patient/dashboard/book', methods=['GET', 'POST'])
@role_required('PATIENT')
def book():
    patient = current_patient()
    doctors = Doctor.query.filter_by(availability=True).order_by(Doctor.last_name.asc()).all()

    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id', type=int)
        date_text = request.form.get('appointment_date', '')
        time_text = request.form.get('appointment_time', '')
        reason = request.form.get('reason', '').strip()[:255]

        doctor = Doctor.query.filter_by(id=doctor_id, availability=True).first() if doctor_id else None
        if doctor is None:
            flash('Please choose an available doctor.', 'error')
            return redirect(url_for('patient.book'))

        try:
            appt_date = datetime.strptime(date_text, '%Y-%m-%d').date()
            appt_time = datetime.strptime(time_text, '%H:%M').time()
        except ValueError:
            flash('Please enter a valid date and time.', 'error')
            return redirect(url_for('patient.book'))

        if datetime.combine(appt_date, appt_time) <= datetime.now():
            flash('Please choose a time in the future.', 'error')
            return redirect(url_for('patient.book'))

        clash = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.appointment_date == appt_date,
            Appointment.appointment_time == appt_time,
            Appointment.status.in_(['Pending', 'Accepted']),
        ).first()
        if clash:
            flash('That time slot is already taken. Please pick another.', 'error')
            return redirect(url_for('patient.book'))

        appointment = Appointment(
            patient_id=patient.id,         
            doctor_id=doctor.id,
            appointment_date=appt_date,
            appointment_time=appt_time,
            reason=reason,
        )
        db.session.add(appointment)
        db.session.commit()

        flash('Appointment requested.', 'success')
        return redirect(url_for('patient.dashboard'))

    return render_template(
        'patient/book_appt.html',
        doctors=doctors,
        today=date.today().isoformat(),
    )


@patient_bp.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@role_required('PATIENT')
def cancel_appointment(appointment_id):
    patient = current_patient()

    # filtering by patient-id is the ownership check
    appointment = Appointment.query.filter_by(
        id=appointment_id, patient_id=patient.id
    ).first_or_404()

    if appointment.status not in ('Pending', 'Accepted'):
        flash('This appointment can no longer be cancelled.', 'error')
        return redirect(url_for('patient.dashboard'))

    appointment.status = 'Cancelled'
    db.session.commit()

    flash('Appointment cancelled.', 'success')
    return redirect(url_for('patient.dashboard'))