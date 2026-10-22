from flask import render_template, redirect, request, flash, url_for
from pkg import db
from pkg.models import Specialty, Doctor, User
from pkg.ADMIN import admin_bp


from flask import session, redirect, url_for, flash, abort

@admin_bp.before_request
def admin_only():
    if 'user_id' not in session:
        flash('Please log in to continue.', 'error')
        return redirect(url_for('auth.login'))
    if session.get('role') != 'ADMINISTRATOR':
        abort(403)

@admin_bp.route('/')
def dashboard():
    specialty_id = request.args.get('specialty_id', type=int)
    search = request.args.get('search', '').strip()

    query = Doctor.query

    if specialty_id:
        query = query.filter(Doctor.specialty_id == specialty_id)

    if search:
        query = query.filter(
            db.or_(
                Doctor.first_name.ilike(f'%{search}%'),
                Doctor.last_name.ilike(f'%{search}%')
            )
        )

    all_doctors = query.order_by(Doctor.last_name.asc()).all()
    specialties = Specialty.query.order_by(Specialty.name.asc()).all()

    return render_template(
        'admin/dashboard.html',
        doctors=all_doctors,
        specialties=specialties,
        selected_specialty=specialty_id,
        search=search
    )

@admin_bp.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    specialties = Specialty.query.all()

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        specialty_id = request.form.get('specialty_id')
        gender = request.form.get('gender')
        licence_no = request.form.get('licence_no', '').strip()
        password = request.form.get('password', '')
        availability = True if request.form.get('availability') == 'on' else False

        if not all([first_name, last_name, email, specialty_id, gender, licence_no, password]):
            flash('Invalid information submitted.', 'error')
            return redirect(url_for('admin.add_doctor'))

        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return redirect(url_for('admin.add_doctor'))

        if Doctor.query.filter_by(email=email).first() or User.query.filter_by(email=email).first():
            flash('An account with this email already exists.', 'error')
            return redirect(url_for('admin.add_doctor'))

        user = User(email=email, role='DOCTOR')
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        new_doctor = Doctor(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            specialty_id=specialty_id,
            gender=gender,
            licence_no=licence_no,
            availability=availability,
        )
        db.session.add(new_doctor)
        db.session.commit()

        flash('Doctor created successfully.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/doctor_form.html', specialties=specialties)


@admin_bp.route('/doctors/edit/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    specialties = Specialty.query.all()

    if not doctor:
        flash('Doctor not found.', 'error')
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        specialty_id = request.form.get('specialty_id')
        gender = request.form.get('gender')
        licence_no = request.form.get('licence_no', '').strip()
        password = request.form.get('password', '')
        availability = True if request.form.get('availability') == 'on' else False

        if not all([first_name, last_name, email, specialty_id, gender, licence_no]):
            flash('Invalid information submitted.', 'error')
            return redirect(url_for('admin.edit_doctor', doctor_id=doctor.id))

        if password and len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return redirect(url_for('admin.edit_doctor', doctor_id=doctor.id))

        doctor_clash = Doctor.query.filter(Doctor.email == email, Doctor.id != doctor.id).first()
        user_clash = User.query.filter(User.email == email, User.id != (doctor.user_id or 0)).first()
        if doctor_clash or user_clash:
            flash('Another account already uses this email.', 'error')
            return redirect(url_for('admin.edit_doctor', doctor_id=doctor.id))

        doctor.first_name = first_name
        doctor.last_name = last_name
        doctor.email = email
        doctor.specialty_id = specialty_id
        doctor.gender = gender
        doctor.licence_no = licence_no
        doctor.availability = availability

        if doctor.user:
            doctor.user.email = email
            if password:
                doctor.user.set_password(password)
        elif password:
            user = User(email=email, role='DOCTOR')
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
            doctor.user_id = user.id

        db.session.commit()

        flash('Doctor updated successfully.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/doctor_form.html', specialties=specialties, doctor=doctor)


@admin_bp.route('/doctors/delete/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)

    if not doctor:
        flash('Doctor not found.', 'error')
        return redirect(url_for('admin.dashboard'))

    user = doctor.user

    db.session.delete(doctor)
    
    if user:
        db.session.delete(user)
    db.session.commit()

    flash('Doctor deleted successfully.', 'success')
    return redirect(url_for('admin.dashboard'))