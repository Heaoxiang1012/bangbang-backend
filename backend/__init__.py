from flask import Flask
from config import Config

from .blueprints.auth import auth_bp
from .blueprints.user import user_bp
from .extensions import db,login_manager,mail

import os


def create_app(config_name=None):
    if config_name==None:
        config_name=os.getenv('FLASK_CONFIG','development')

    app = Flask(__name__)
    app.config.from_object(Config[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_commands(app)

    return app

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

def register_commands(app):
    @app.cli.command()
    def initdb():
        db.drop_all()
        db.create_all()

