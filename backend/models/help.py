from ..extensions import db
from ..models.user import User



class Help(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    declaration = db.Column(db.String(50), nullable=False) # 辅导者自我介绍
    type = db.Column(db.Boolean,default=False) #默认为course

    major = db.Column(db.String(50), nullable=False)  # 辅导课程名
    price = db.Column(db.Float, default=0.00)  # 价格，可为空
    grade = db.Column(db.Float(5), nullable=False)  # 辅导者该课程绩点

    release_date = db.Column(db.TIMESTAMP, nullable=False)  # 辅导信息发布日期

    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 设置外键，关联用户表
    user = db.relationship('User',back_populates='helps') #用户发布的辅导

'''

# 预约信息表
class Order(db.Model):
     id = db.Column(db.Integer,primary_key=True)
     date = db.Column(db.TIMESTAMP,nullable=False) # 预约发起时间
     state = db.Column(db.Integer,nullable=False) # 是否同意预约（0/1）

     help_id = db.Column(db.Integer,db.ForeignKey('Help.id')) # 外键，关联辅导表
     user_id = db.Column(db.Integer,db.ForeignKey('User.id')) # 外键，关联用户表

# 评价表
class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.Text,nullable=False) # 评价内容

    help_id = db.Column(db.Integer,db.ForeignKey('Help.id')) # 外键，关联辅导表
    order_id = db.Column(db.Integer,db.ForeignKey('Order.id')) # 外键，关联预约信息表

'''