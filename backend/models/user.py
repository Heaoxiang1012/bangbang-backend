from ..extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(16),unique=True,nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(256),unique=True,nullable=False)
    nickname = db.Column(db.String(16),unique=True,nullable=False)
    signature = db.Column(db.String(128))
    is_verify = db.Column(db.Boolean,default=False)
    find_passwd = db.Column(db.Integer) #用于找回密码

    number = db.Column(db.String(8),unique=True)
    _password = db.Column(db.String(128))

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
