from ..extensions import db
from ..models.user import User



class Help(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    declaration = db.Column(db.String(50), nullable=False) # 辅导者自我介绍
    type = db.Column(db.Boolean,default=False) #默认为course

    major = db.Column(db.String(50), nullable=False)  # 辅导课程名
    price = db.Column(db.Float, default=0.00)  # 价格，可为空
    grade = db.Column(db.String(8), nullable=False)  # 辅导者该课程绩点

    release_date = db.Column(db.TIMESTAMP, nullable=False)  # 辅导信息发布日期

    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 设置外键，关联用户表
    user = db.relationship('User',back_populates='helps') #用户发布的辅导
    orders = db.relationship('Order',back_populates='help')

    comments = db.relationship('Comment',back_populates='help')  #预约的辅导

# 预约信息表
class Order(db.Model):
     id = db.Column(db.Integer,primary_key=True)
     date = db.Column(db.TIMESTAMP,nullable=False) # 预约发起时间
     state = db.Column(db.Boolean,nullable=False,default=False) # 是否同意预约（0/1）
     is_pay = db.Column(db.Boolean,nullable=False,default=False)

     help_id = db.Column(db.Integer,db.ForeignKey('help.id')) # 外键，关联辅导表
     be_user_id = db.Column(db.Integer,db.ForeignKey('user.id')) # 外键,发起预约人的id

     help = db.relationship('Help',back_populates='orders')  #预约的辅导
     be_user = db.relationship('User',back_populates='orders')  #预约的人


# 评价表
class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.Text,nullable=False) # 评价内容

    help_id = db.Column(db.Integer,db.ForeignKey('help.id')) # 外键，关联辅导表
    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) # 外键，关联预约信息表

    help = db.relationship('Help',back_populates='comments')  #预约的辅导
    user = db.relationship('User',back_populates='comments')  #预约的辅导

