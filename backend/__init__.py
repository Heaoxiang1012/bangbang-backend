from flask import Flask
from config import Config

from .blueprints.auth import auth_bp
from .blueprints.user import user_bp
from .blueprints.help import help_bp
from .blueprints.note import note_bp
from .blueprints.msg import msg_bp
from .blueprints.admin import admin_bp
from .blueprints.assist import assist_bp

from .extensions import db,login_manager,mail,socketio,avatars
from .models.help import Help,Order
from .models.user import User
from .models.note import File,Note
from .models.assist import Couple

import os

def create_app(config_name=None):
    if config_name==None:
        config_name=os.getenv('FLASK_CONFIG','development')

    app = Flask(__name__)
    app.config.from_object(Config[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    register_shell_context(app)

    return app

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(help_bp, url_prefix='/coach')
    app.register_blueprint(note_bp, url_prefix='/note')
    app.register_blueprint(msg_bp,  url_prefix='/msg')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(assist_bp, url_prefix='/assist')

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    avatars.init_app(app)

def register_commands(app):
    @app.cli.command()
    def initdb():
        db.drop_all()
        db.create_all()

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db,User=User,Help=Help,Order=Order,Note=Note,File=File)



