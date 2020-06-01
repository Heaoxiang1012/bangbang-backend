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
    signature = db.Column(db.String(128),default='这个人很懒，什么都没留下。')#默认签名
    is_verify = db.Column(db.Boolean,default=False)
    find_passwd = db.Column(db.Integer) #用于找回密码
    avatar = db.Column(db.String(64))

    number = db.Column(db.String(8),unique=True)
    _password = db.Column(db.String(128))
    real_name = db.Column(db.String(16))

    star = db.Column(db.Float,default=0.0) #平均星级
    count = db.Column(db.Integer,default=0) #被评价次数
    is_admin = db.Column(db.Boolean,default=False) #是否是管理员

    helps = db.relationship('Help',back_populates='user') #用户发布的辅导
    orders = db.relationship('Order',back_populates='be_user') #发起的预约
    notes = db.relationship('Note',back_populates='user')
    comps = db.relationship('Compliments',back_populates='user')

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

