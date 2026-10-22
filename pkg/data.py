from pkg import create_app, db
from pkg.models import Specialty, Doctor

app = create_app()

with app.app_context():
    specialty_names = [
        "Cardiology",
        "Dermatology",
        "Paediatrics",
        "General Medicine",
        "Orthopaedics",
    ]

    specialties = {}
    for name in specialty_names:
        existing = Specialty.query.filter_by(name=name).first()
        if existing:
            specialties[name] = existing
        else:
            specialty = Specialty(name=name)
            db.session.add(specialty)
            specialties[name] = specialty

    db.session.commit()



    doctors_data = [
        ("Ade", "Bello", "ade.bello@carepoint.com", "Cardiology", "M", "LIC001"),
        ("Chiamaka", "Okoye", "chiamaka.okoye@carepoint.com", "Cardiology", "F", "LIC002"),
        ("Tunde", "Adeyemi", "tunde.adeyemi@carepoint.com", "Dermatology", "M", "LIC003"),
        ("Ngozi", "Eze", "ngozi.eze@carepoint.com", "Dermatology", "F", "LIC004"),
        ("Femi", "Ogundipe", "femi.ogundipe@carepoint.com", "Paediatrics", "M", "LIC005"),
        ("Bisi", "Fashola", "bisi.fashola@carepoint.com", "Paediatrics", "F", "LIC006"),
        ("Musa", "Ibrahim", "musa.ibrahim@carepoint.com", "General Medicine", "M", "LIC007"),
        ("Kemi", "Afolabi", "kemi.afolabi@carepoint.com", "Orthopaedics", "F", "LIC008"),
    ]

    for first, last, email, specialty_name, gender, licence_no in doctors_data:
        existing = Doctor.query.filter_by(email=email).first()
        if not existing:
            doctor = Doctor(
                first_name=first,
                last_name=last,
                email=email,
                specialty=specialties[specialty_name],
                gender=gender,
                licence_no=licence_no,
                availability=True,
            )
            db.session.add(doctor)

    db.session.commit()

    print("Seeding complete.")