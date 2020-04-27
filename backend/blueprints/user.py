import json
import os


from flask import Blueprint,request,current_app,send_from_directory
from flask_login import current_user,login_user,logout_user
from ..models.user import User
from ..extensions import db
from ..util_verify import get_marks
from ..utils import random_filename


user_bp = Blueprint('user',__name__)


@user_bp.before_request
def login_project():
    route = ['avatar']
    method = request.method
    ext = request.path
    flag = False


    for i in route :
        if i in ext :
            flag = True

    if method == 'GET' and flag :
        pass

    else :
        result = {}
        if current_user.is_authenticated == False:
            result['code'] = -1
            result['msg'] = '您当前未登录！'
            return json.dumps(result)

        else :
            id =current_user.get_id()
            user = User.query.get(id)

            if user.is_verify == False:
                result['code'] = -2
                result['msg'] = '请先实名制认证！'
                return json.dumps(result)


@user_bp.route('/grade',methods=['GET'])
def grade():
    id = current_user.get_id()
    user = User.query.get(id)

    results = get_marks(id,user.number,user._password)

    return json.dumps(results)

@user_bp.route('/change_password',methods=['POST'])
def change_password():
    results = {}
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    id = current_user.get_id()
    user = User.query.get(id)

    if user.check_password(old_password) == False :
        results['code'] = 1
        results['msg'] = current_app.config['CHANGE_PASSWD'][1]

    elif len(new_password)<6 and len(new_password)>16:
        results['code'] = 2
        results['msg'] = current_app.config['CHANGE_PASSWD'][2]

    else :
        results['code'] = 0
        results['msg'] = current_app.config['CHANGE_PASSWD'][0]
        user.set_password(new_password)
        db.session.commit()

    return json.dumps(results)

@user_bp.route('/profile',methods=['GET'])
@user_bp.route('/profile/<int:uid>',methods=['GET'])
def profile(uid=-1):
    results = {}

    if uid == -1 :
        uid = current_user.get_id()

    user = User.query.get(uid)

    data = {
        'uid' : int(uid),
        'username' : user.username,
        'email' : user.email,
        'nickname' : user.nickname,
        'signature' : user.signature
    }

    results['code'] = 0
    results['msg'] = '获取资料成功'
    results['data'] = data

    return json.dumps(results)

@user_bp.route('/profile',methods=['POST'])
def set_profile():
    results = {}
    nickname = request.form.get('nickname')
    signature = request.form.get('signature')

    id = current_user.get_id()
    user = User.query.get(id)

    user.signature = signature
    user.nickname = nickname

    db.session.commit()

    results['code'] = 0
    results['msg'] = '修改成功'

    return json.dumps(results)

@user_bp.route('/avatar',methods=['GET'])
@user_bp.route('/avatar/<int:uid>',methods=['GET'])
def get_avatar(uid):

    if uid == None :
        uid = current_user.get_id()

    user = User.query.get(uid)

    filename = user.avatar

    return send_from_directory(current_app.config['AVATAR_PATH'],filename)


@user_bp.route('/avatar',methods=['POST'])
def set_avatar():
    results = {}
    f = request.files.get('avatar')

    id = current_user.get_id()
    user = User.query.get(id)

    filename = random_filename(f.filename)
    f.save(os.path.join(current_app.config['AVATAR_PATH'], filename))

    user.avatar = filename

    db.session.commit()

    results['code'] = 0
    results['msg'] = '修改成功'

    return  json.dumps(results)
















