import json
from datetime import datetime

from flask import Blueprint,request,current_app,send_from_directory
from flask_login import current_user,login_user,logout_user
from ..models.msg import Message
from ..extensions import db,socketio
from ..models.user import User
from flask_socketio import emit,join_room


msg_bp = Blueprint('msg',__name__)

@socketio.on('join',namespace='/chat')
def join():
    id = current_user.id
    join_room(id)


@socketio.on('getmsg',namespace='/chat')
def get_msg(msg):
    msg = json.loads(msg)
    room = msg['room'] #user_id
    text = msg['text']#消息内容

    user = User.query.get(room)

    message = Message(
        from_user_id = current_user.id,
        to_user_id = room,
        date = datetime.today(),
        content = text,
    )

    db.session.add(message)
    db.session.commit()

    user2 = User.query.get(current_user.id)

    data = {
        'room': current_user.id,
        'content': text,
        'user_nickname': user2.nickname
    }

    results = {
        'code' :0,
        'msg' : '转发成功',
        'data' : data,
    }

    emit('sendmsg',json.dumps(results),room=room)


@msg_bp.route('/msglist',methods=['GET'])
def get_msglist():
    results = {}

    data = []
    data1 = {}

    uid = current_user.id

    from_messages = Message.query.filter_by(from_user_id=uid).order_by(Message.date.desc()).all() #发送方是登录用户
    to_messages = Message.query.filter_by(to_user_id=uid).order_by(Message.date.desc()).all()  #接收方是登录用户

    if from_messages is not None or to_messages is not None :

        for message in from_messages:
            if message.to_user_id not in data1.keys() :
                data1[message.to_user_id] = message

        for message in to_messages:
            if message.from_user_id not in data1.keys() :
                data1[message.from_user_id] = message

            else :
                if message.date > data1[message.from_user_id].date :
                    data1[message.from_user_id] = message


        for message in data1.values():

            if message.from_user_id != 0 :
                id = message.from_user_id
                if id == current_user.id :
                    id = message.to_user_id

                user = User.query.get(id)

                d = {
                    'user_id' : id,
                    'last_message' : message.content,
                    'date' : int(message.date.timestamp()),
                    'user_nickname' : user.nickname
                }
                data.append(d)

            else :
                d = {
                    'user_id': 0,
                    'last_message': message.content,
                    'date': int(message.date.timestamp()),
                    'user_nickname': '系统消息'
                }
                data.append(d)

    results['code'] = 0
    results['msg'] = '返回成功'
    results['data'] = data

    return json.dumps(results)

@msg_bp.route('/history',methods=['GET'])
def history():
    results = {}
    data = []
    Data = []
    uid = current_user.id
    uuid = int(request.args.get('user_id'))


    if uuid != 0 :
        user = User.query.get(uuid)
        message1 = Message.query.filter_by(from_user_id=uid,to_user_id=uuid).order_by(Message.date.desc()).all()
        message2 = Message.query.filter_by(from_user_id=uuid,to_user_id=uid).order_by(Message.date.desc()).all()

        for message in message1 :
            d = {
                'from_user_id' : message.from_user_id,
                'to_user_id' : message.to_user_id,
                'content' : message.content,
                'date' :int(message.date.timestamp())
            }
            data.append(d)

        for message in message2 :
            d = {
                'from_user_id' : message.from_user_id,
                'to_user_id' : message.to_user_id,
                'content' : message.content,
                'date' : int(message.date.timestamp())
            }
            data.append(d)

        for d in sorted(data,key= lambda s:s['date']):
            Data.append(d)

        results['code'] = 0
        results['msg'] = '查看成功'
        results['data'] = Data
        results['user_nickname'] = user.nickname

    else :
        messages = Message.query.filter_by(from_user_id=0, to_user_id=uid).order_by(Message.date.desc()).all()
        for message in messages :
            d = {
                'from_user_id' : message.from_user_id,
                'to_user_id' : message.to_user_id,
                'content' : message.content,
                'date' :int(message.date.timestamp())
            }
            data.append(d)

        results['code'] = 0
        results['msg'] = '查看成功'
        results['data'] = data
        results['user_nickname'] = '系统消息'

    return json.dumps(results)

#tetpy