from datetime import datetime, date
from flask import render_template, request, redirect, url_for, flash, session
from pkg import db
from pkg.models import User, Patient
from pkg.AUTH import auth_bp


ROLE_HOME = {
    'PATIENT': 'patient.dashboard',
    'DOCTOR': 'doctor.dashboard',
    'ADMINISTRATOR': 'admin.dashboard',
}


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash('Invalid email or password.', 'error')
            return redirect(url_for('auth.login'))

        session.clear()
        session['user_id'] = user.id
        session['role'] = user.role

        return redirect(url_for(ROLE_HOME[user.role]))

    return render_template('auth/login.html')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        fullname = request.form.get('fullname', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        phone = request.form.get('phone', '').strip()
        dob_text = request.form.get('dob', '')

        if not all([fullname, email, password, confirm, dob_text]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('auth.reg'))

        parts = fullname.split(None, 1)
        if len(parts) < 2:
            flash('Please enter your first and last name.', 'error')
            return redirect(url_for('auth.reg'))
        first_name, last_name = parts

        try:
            dob = datetime.strptime(dob_text, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date of birth.', 'error')
            return redirect(url_for('auth.reg'))

        if dob >= date.today():
            flash('Date of birth must be in the past.', 'error')
            return redirect(url_for('auth.reg'))

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.reg'))

        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
            return redirect(url_for('auth.reg'))

        if User.query.filter_by(email=email).first():
            flash('An account with this email already exists.', 'error')
            return redirect(url_for('auth.reg'))

        user = User(email=email, role='PATIENT')
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        patient = Patient(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            date_of_birth=dob,
        )
        db.session.add(patient)
        db.session.commit()

        flash('Account created. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')