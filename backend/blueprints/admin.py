import json
import random
import os

from flask import Blueprint,request
from flask_login import current_user,login_user,logout_user

from ..models.user import User
from ..models.assist import Assistant,Assisted,Couple

from ..extensions import db
from ..utils import check_register_form,send_mail,random_filename
from ..util_verify import get_name

admin_bp = Blueprint('admin',__name__)

@admin_bp.before_request
def login_project():
    route = ['avatar','file']
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

            if user.is_verify == False and user.is_admin == False:
                result['code'] = -2
                result['msg'] = '请先实名制认证！'
                return json.dumps(result)

            elif user.admin == False :
                result['code'] = -3
                result['msg'] = '权限不够！'
                return json.dumps(result)

@admin_bp.route('/add',methods=['POST'])
def add_user():
    results = {}
    nickname = request.form.get('nickname')
    course = request.form.get('course')

    user = User.query.filter_by(nickname=nickname).first()

    if user != None :
        assist = Assisted(
            user_id = user.id,
            course = course,
        )
        db.session.add(assist)
        db.session.commit()
        results['code'] = 0
        results['msg'] = '添加成功'

    else :
        results['code'] = 1
        results['msg'] = '无此用户！'

    return json.dumps(results)


@admin_bp.route('/list',methods=['GET'])
def list():
    results = {}
    data = []
    couples = Couple.query.filter_by(status=0).all()

    if couples != None :
        for couple in couples :
            assistant_id = couple.user_id
            assisted_id = couple.be_user_id
            assistant = User.query.get(assistant_id)
            assisted = User.query.get(assisted_id)

            d = {
                'couple_id' : couple.id,
                'assistant_id' : assistant_id ,#帮扶人id
                'assistant_nickname' : assistant.nickname, #帮扶人昵称
                'assisted_id' :   assisted_id ,#被帮扶人id
                'assisted_nickname' :  assisted.nickname ,#被帮扶人昵称
            }
            data.append(d)
        results['code'] = 0
        results['msg'] = '返回成功'
        results['data'] = data

    return json.dumps(results)

@admin_bp.route('/approve',methods=['POST'])
def approve():
    results = {}
    couple_id = request.form.get('couple_id')

    couple = Couple.query.get(couple_id)

    couple.status = 1

    db.session.commit()

    results['code'] = 0
    results['msg'] = '批准成功'

    return json.dumps(results)
