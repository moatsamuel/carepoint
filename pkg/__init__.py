from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from pkg.config import GeneralConfig
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(GeneralConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from pkg import models

    from pkg.main import main_bp
    from pkg.AUTH import auth_bp
    from pkg.PATIENT import patient_bp
    from pkg.ADMIN import admin_bp
    from pkg.DOCTOR import doctor_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(doctor_bp)

    return app

