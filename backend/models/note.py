from ..extensions import db
from ..models.user import User


class Note(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)  # 标题
    compliments = db.Column(db.Integer, default=0)  # 点赞数
    note_date = db.Column(db.TIMESTAMP, nullable=False)  # 笔记最近一次更新时间
    tag = db.Column(db.String(32),nullable=False)
    content = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  #谁发布的

    user = db.relationship('User', back_populates='notes')  # 用户
    comps = db.relationship('Compliments', back_populates='note')


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128),nullable=False,unique=True)

class Compliments(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 谁点赞的
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))  # 谁点赞的

    note = db.relationship('Note', back_populates='comps')  # 用户
    user = db.relationship('User', back_populates='comps')  # 用户


    #class Note(db.Model):
    #note_id = db.Column(db.Integer, Primary_key=True)

    #u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user = db.relationship('User', back_populates='notes')

    #category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    #category = db.relationship('Category', back_populates='notes')

    #title = db.Column(db.String(50), nullable=False)
    #compliments = db.Column(db.Integer, default=0)
    #note_date = db.Column(db.TIMESTAMP, nullable=False)
    #content = db.Column(db.TEXT, nullable=False)
    #image_name = db.Column(db.String(64), nullable=True)
    #file_name = db.Column(db.String(64), nullable=True)