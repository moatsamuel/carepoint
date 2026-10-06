from pkg import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Specialty(db.Model):
    __tablename__ = 'specialty'

    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    name = db.Column(db.String(200), nullable = False, index = True,unique = True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    doctors = db.relationship("Doctor", backref = 'specialty')


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(200), nullable=False, index=True)
    last_name = db.Column(db.String(200), nullable=False, index=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    specialty_id = db.Column(db.Integer, db.ForeignKey("specialty.id"), nullable=False)
    availability = db.Column(db.Boolean, default=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    licence_no = db.Column(db.String(50), unique=True, nullable=False)
    consultation_fee = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)   # <-- NEW
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=True)
    user = db.relationship("User", backref=db.backref("doctor", uselist=False))



class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.String(255), nullable=True)

    status = db.Column(
        db.Enum('Pending', 'Accepted', 'Rejected', 'Cancelled', 'Completed', name='appointment_status'),
        default='Pending',
        nullable=False
    )
    patient =  db.relationship("Patient", backref="appointments")
    doctor =  db.relationship("Doctor", backref="appointments")


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.Enum('PATIENT', 'DOCTOR', 'ADMINISTRATOR', name='user_role'),
        default='PATIENT',
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("patient", uselist=False))