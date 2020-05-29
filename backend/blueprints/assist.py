import json
import random
import os
from datetime import datetime

from flask import Blueprint,request,current_app
from flask_login import current_user,login_user,logout_user

from ..models.user import User
from ..models.assist import Assistant,Assisted,Couple,Pickup
from ..models.note import File

from ..extensions import db
from ..utils import check_register_form,send_mail,random_filename
from ..util_verify import get_name
from werkzeug.security import check_password_hash


assist_bp = Blueprint('assist',__name__)

@assist_bp.before_request   #!@#!@#
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
        if current_user.is_authenticated == False :
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
                'course' : assisted.course,
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

    id = current_user.id

    if id == user_id :
        results['code'] = 1
        results['msg'] = '请勿申请自己发起的帮扶'
    else :
        course_token = request.form.get('course_token')
        course = request.form.get('course')
        grade = request.form.get('grade')
        complement = request.form.get('complement')

        token = str(id) + str(course) + str(grade)

        if check_password_hash(course_token, token) == False:
            results['code'] = -1
            results['msg'] = "成绩有误！"

        else :
            cc = Couple.query.filter_by(user_id=id,be_user_id=user_id).first()

            if cc == None:
                couple = Couple(
                    user_id = id,
                    be_user_id = user_id,
                    complement = complement,
                    course = course,
                    grade = grade,
                )

                db.session.add(couple)
                db.session.commit()

                results['code'] = 0
                results['msg'] = '申请成功'

            else :
                results['code'] = 1
                results['msg'] = '请勿重复申请'

        return json.dumps(results)

@assist_bp.route('/myassist',methods=['GET'])
def myassist():
    results = {}
    data = []
    couples = Couple.query.filter_by(user_id=current_user.id,status=1).all() #

    if couples != None :
        for couple in couples :
            be_user = User.query.filter_by(id=couple.be_user_id).first()
            assisted = Assisted.query.filter_by(user_id=couple.be_user_id).first()
            d = {
                'couple_id' : couple.id,
                'assisted_nickname': be_user.nickname,
                'assisted_id' : be_user.id,
                'course' : assisted.course,
            }
            data.append(d)

    results['code'] = 0
    results['msg'] = '查看成功'
    results['data'] = data

    return  json.dumps(results)

@assist_bp.route('/pickup',methods=['POST'])
def pickup():
    results = {}
    couple_id = request.form.get('couple_id')
    file = request.files.get('file')

    filename = random_filename(file.filename)
    file.save(os.path.join(current_app.config['PICK_UP_PATH'], filename))

    f = File(
        filename = filename
    )
    db.session.add(f)
    db.session.commit()

    pick_up = Pickup(
        couple_id = couple_id,
        date = datetime.today(),
        file_id = f.id,
    )

    db.session.add(pick_up)
    db.session.commit()

    results['code'] = 0
    results['msg'] = '打卡成功'

    return json.dumps(results)

@assist_bp.route('/reward',methods=['POST'])
def reward():
    results = {}
    couple_id = request.form.get('couple_id')
    couple = Couple.query.get(couple_id)

    couple.status = 2
    db.session.commit()

    results['code'] = 0
    results['msg'] = '申请成功'
    return json.dumps(results)
