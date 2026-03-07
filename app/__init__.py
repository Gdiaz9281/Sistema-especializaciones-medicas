from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres123@localhost:5432/bienestar_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)
    from app import models

    from app.especializaciones.routes import bp_especializaciones
    app.register_blueprint(bp_especializaciones)

    return app