from ..extensions import db


class Assisted(db.Model):
    id = db.Column(db.Integer, primary_key=True) #帮扶对象

    course = db.Column(db.String(32)) #帮扶课程part
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
    status = db.Column(db.Integer,default=0) #0未批准 1批准 2申请综测中  3帮扶结束
    complement = db.Column(db.String(128))

    course =  db.Column(db.String(32)) #帮扶课程
    grade = db.Column(db.String(8) )  # 辅导者该课程绩点
    charter = db.Column(db.String(128)) #唯一凭证

    pickups = db.relationship('Pickup', back_populates='couple')

class Pickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.TIMESTAMP, nullable=False)  # 打卡日期part

    file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
    couple_id = db.Column(db.Integer, db.ForeignKey('couple.id'))  #帮扶couple

    couple = db.relationship('Couple', back_populates='pickups')
