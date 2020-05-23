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

assist_bp = Blueprint('assist',__name__)

#@assist_bp.before_request   #!@#!@#
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

@assist_bp.route('',methods=['GET'])
def index():
    results = {}
    data = []
    assisteds = Assisted.query.filter_by(status=0).all()

    if assisteds != None:
        for assisted in assisteds:
            user = User.query.get(assisted.user_id)
            d = {
                'user_id' : assisted.user_id,
                'user_nickname' : user.nickname,
                'course' : assisted.course
            }
            data.append(d)

    results['code'] = 0
    results['msg'] = '返回成功'
    results['data'] = data

    return json.dumps(results)

@assist_bp.route('/apply',methods=['POST'])
def apply():
    results = {}
    user_id = int(request.form.get('user_id'))

    id = 1#current_user.id

    if id == user_id :
        results['code'] = 1
        results['msg'] = '请勿申请自己发起的帮扶'

    else :
        couple = Couple(
            user_id = id,
            be_user_id = user_id,
        )

        db.session.add(couple)
        db.session.commit()

        results['code'] = 0
        results['msg'] = '申请成功'

    return json.dumps(results)



