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

    with app.app_context():
        from pkg import routes
        from pkg import models


    
    return app

