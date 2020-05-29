from ..extensions import db


class Assisted(db.Model):
    id = db.Column(db.Integer, primary_key=True) #帮扶对象

    course = db.Column(db.String(32)) #帮扶课程

    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) #user id
    status = db.Column(db.Integer,default=0) #0后台加入 1后台批准 2帮扶结束

class Assistant(db.Model):
    id = db.Column(db.Integer, primary_key=True) #帮扶人

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # user id
    status = db.Column(db.Integer, default=0)  # 0申请帮扶 1后台批准 2帮扶结束

class Couple(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('assistant.id')) #帮扶人
    be_user_id = db.Column(db.Integer, db.ForeignKey('assisted.id')) #帮扶对象
    status = db.Column(db.Integer,default=0) #0未批准 1批准 2帮扶结束

    pickups = db.relationship('Pickup', back_populates='couple')

class Pickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.TIMESTAMP, nullable=False)  # 打卡日期

    filename = db.Column(db.String(128),nullable=False,unique=True)
    couple_id = db.Column(db.Integer, db.ForeignKey('couple.id'))  #帮扶couple

    couple = db.relationship('Couple', back_populates='pickups')

    #class Category(db.Model):
    #category_id = db.Column(db.Integer, Primary_key=True)
    #category_name = db.Column(db.String(50), unique=True)

    #notes = db.relationship('Note', back_populates='category')  # 用户发布的笔记

    #*********测试提交
    #user_id = db.Column(db.Integer, db.ForeignKey('assistant.id')) #帮扶人
    #be_user_id = db.Column(db.Integer, db.ForeignKey('assisted.id')) #帮扶对象
    #status = db.Column(db.Integer,default=0) #0未批准 1批准 2帮扶结束
