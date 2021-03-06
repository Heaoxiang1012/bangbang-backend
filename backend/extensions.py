from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_avatars import Avatars

db  = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
socketio = SocketIO()
avatars = Avatars()

login_manager.login_view = 'auth.login'
@login_manager.user_loader
def load_user(admin_id):
    from .models.user import User
    admin = User.query.get(int(admin_id))
    return admin
