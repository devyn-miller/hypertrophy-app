from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import config_by_name
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

from .views.auth import auth
from .views.training import training
from .views.nutrition import nutrition
from .views.progress import progress

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(training)
    app.register_blueprint(nutrition)
    app.register_blueprint(progress)

    return app
