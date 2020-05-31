from ..extensions import db
from ..models.user import User

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) #聊天记录id

    date = db.Column(db.TIMESTAMP, nullable=False)  # 消息发送时间
    content = db.Column(db.Text, nullable=False, default=False)  # 发送内容

    status = db.Column(db.Boolean, nullable=False, default=True) #接收状态

    from_user_id = db.Column(db.Integer, db.ForeignKey('help.id'))  # 发送消息人id
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 外键,接收消息人id

#test
#msg_bp = Blueprint('msg',__name__)

#@socketio.on('join',namespace='/chat')
#def join():
    #id = current_user.id
    #join_room(id)

