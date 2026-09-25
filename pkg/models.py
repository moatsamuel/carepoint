from pkg import db
from datetime import datetime


class Specialty(db.Model):
    __tablename__ = 'Specialty'

    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    name = db.Column(db.String(200), nullable = False, index = True,unique = True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    doctors = db.relationship("Doctor", backref = 'specialty')


class Doctor(db.Model):
    __tablename__ = 'Doctors'

    id = db.Column(db.Integer,primary_key =True, autoincrement = True)
    first_name = db.Column(db.String(200), nullable = False, index = True,)
    last_name = db.Column(db.String(200), nullable = False, index = True,)
    email = db.Column(db.String(200),nullable = False,unique = True)
    specialty_id = db.Column(db.Integer,db.ForeignKey("Specialty.id"),nullable = False)
    availabilty = db.Column(db.Boolean, default = True, nullable = False)
    gender = db.Column(db.String(10),nullable = False)
    licence_no = db.Column(db.String(50),unique = True, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)