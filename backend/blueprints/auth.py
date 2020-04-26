import json
import random

from flask import Blueprint,request,current_app
from flask_login import current_user,login_user,logout_user

from ..models.user import User
from ..extensions import db
from ..utils import check_register_form,send_mail
from ..util_verify import get_name

auth_bp = Blueprint('auth',__name__)

Msg = ['注册成功','用户名已存在','Email已存在','用户名长度必须在3-16个字符之间','密码长度必须在6-16位之间','Email格式不正确','昵称长度必须在3-16个字符之间']

@auth_bp.route('/register',methods=['POST'])
def register():
    results = {}

    username = request.form.get('username')
    password = request.form.get('password')
    nickname = request.form.get('nickname')
    email = request.form.get('email')
    code = check_register_form(username,password,nickname,email)

    msg = Msg[code]

    if code == 0 :
        user = User(
            username=username,
            nickname=nickname,
            email=email
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    results['code'] = code
    results['msg'] = msg

    return json.dumps(results)

@auth_bp.route('/login',methods=['POST'])
def login():
    results = {}

    code = 0
    msg ='登录成功'
    data = {}

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user is None  or user.check_password(password) == False :
        code = 1
        msg = '用户名或密码错误'

    else :
        login_user(user)
        data['token'] = current_user.get_id()
        results['data'] = data

    results['code'] = code
    results['msg'] = msg

    return json.dumps(results)

@auth_bp.route('/forget_password/send',methods=['POST'])
def send_forget_password():
    results = {}
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if user is None:
        results['code'] = 1
        results['msg'] = current_app.config['SEND_EMAIL'][1]
    else :
        subject = '学长帮帮忙————找回密码'
        recipients = email
        body = random.randint(1000,9999)

        user.find_passwd = body
        db.session.commit()

        send_mail(subject,recipients,body)

        results['code'] = 0
        results['msg'] = current_app.config['SEND_EMAIL'][0]

    return json.dumps(results)

@auth_bp.route('/forget_password',methods=['POST'])
def forget_password():
    results = {}
    email = request.form.get('email')
    password = request.form.get('password')
    verify_code = request.form.get('verify_code')

    user = User.query.filter_by(email=email).first()
    if user is None:
        results['code'] = 1
        results['msg'] = current_app.config['FORGET_PASSWD'][1]

    elif verify_code != user.find_passwd:
        results['code'] = 2
        results['msg'] = current_app.config['FORGET_PASSWD'][2]

    elif len(password)<6 and len(password)>16:
        results['code'] = 3
        results['msg'] = current_app.config['FORGET_PASSWD'][3]

    else :
        user.set_password(password)
        db.session.commit()
        results['code'] = 0
        results['msg'] = current_app.config['FORGET_PASSWD'][0]

    return json.dumps(results)

@auth_bp.route('/verify', methods=['POST'])
def verify():
    if current_user.is_authenticated == False:
        results = {}
        results['code'] = -1
        results['msg'] = '您当前未登录！'
        return json.dumps(results)

    number = request.form.get('number')
    _password = request.form.get('password')

    id = current_user.get_id()
    user = User.query.get(id)

    user._password = _password
    user.number = number
    user.is_verify = True
    db.session.commit()
    results = get_name(number, _password)

    return json.dumps(results)



