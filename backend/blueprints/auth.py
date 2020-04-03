import json

from flask import Blueprint,request
from flask_login import current_user,login_user,logout_user

from ..models.user import User
from ..extensions import db
from ..utils import check_register_form

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

@auth_bp.route('login',methods=['POST'])
def login():
    results = {}

    code = 0
    msg ='登录成功'
    data = {}

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user.check_password(password) == False or user is None:
        code = 1
        msg = '用户名或密码错误'


    else :
        login_user(user)
        data['token'] = current_user.get_id()
        results['data'] = data

    results['code'] = code
    results['msg'] = msg

    return json.dumps(results)
