import json
import random
import os

from flask import Blueprint,request,send_from_directory,current_app
from flask_login import current_user,login_user,logout_user

from ..models.user import User
from ..models.assist import Assistant,Assisted,Couple
from ..models.note import File

from ..extensions import db
from ..utils import check_register_form,send_mail,random_filename
from ..util_verify import get_name
from werkzeug.security import generate_password_hash


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

            elif user.is_admin == False :
                result['code'] = -3
                result['msg'] = '权限不够！'
                return json.dumps(result)

@admin_bp.route('/add',methods=['POST'])
def add_user():
    results = {}
    id  = request.form.get('user_id')
    course = request.form.get('course')

    user = User.query.get(id)

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

    assists = Assisted.query.all()

    for assist in assists :
        be_user_id = assist.user_id
        couples = Couple.query.filter_by(be_user_id=be_user_id,status=0).all()
        if couples != None :
            be_user = User.query.get(assist.user_id)
            d = {
                'assisted_id' :   assist.id ,#被帮扶人id
                'assisted_nickname' :  be_user.nickname ,#被帮扶人昵称
                'assisted_course' : assist.course,
            }
            dd = []
            for couple in couples :
                user_id = couple.user_id
                user = User.query.get(user_id)
                ddd = {
                    'couple_id' : couple.id,
                    'assistant_nickname' : user.nickname,
                    'assistant_id' : couple.user_id,
                    'complement' : couple.complement,
                    'course' : couple.course,
                    'grade' : couple.grade,
                }
                dd.append(ddd)
            d['assistants'] = dd
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

    be_user_id = couple.be_user_id
    assisted = Assisted.query.get(be_user_id)
    assisted.status = 1

    db.session.commit()

    results['code'] = 0
    results['msg'] = '批准成功'

    return json.dumps(results)


@admin_bp.route('/pickup',methods=['GET'])
def pickup():
    couple_id = request.args.get('couple_id')
    couple = Couple.query.get(couple_id)
    results = {}
    data = []

    pickups = couple.pickups
    if pickups != None :

        for pickup in pickups :

            d = {
                'date' : pickup.date.strftime('%Y-%m-%d'),
                'file_id' : pickup.file_id,
            }

            data.append(d)

    results['code'] = 0
    results['msg'] = '添加成功'
    results['data'] = data

    return json.dumps(results)


@admin_bp.route('/file/<int:id>',methods=['GET'])
def get_file(id):
    file = File.query.get(id)
    filename = file.filename

    return send_from_directory(current_app.config['PICK_UP_PATH'], filename)

@admin_bp.route('/rewardlist',methods=['GET'])
def rewardlist():
    results = {}
    data = []
    couples = Couple.query.filter_by(status=2).all()

    if couples != None:
        for couple in couples:
            assistant_id = couple.user_id
            assisted_id = couple.be_user_id
            assistant = User.query.get(assistant_id)
            assisted = User.query.get(assisted_id)

            d = {
                'couple_id': couple.id,
                'assistant_id': assistant_id,  # 帮扶人id
                'assistant_nickname': assistant.nickname,  # 帮扶人昵称
                'assisted_id': assisted_id,  # 被帮扶人id
                'assisted_nickname': assisted.nickname,  # 被帮扶人昵称
                'complement': couple.complement,
                'days': len(couple.pickups),
                'course' : couple.course,
            }
            data.append(d)
        results['code'] = 0
        results['msg'] = '返回成功'
        results['data'] = data

    return json.dumps(results)

@admin_bp.route('/reward',methods=['POST'])
def reward():
    couple_id = request.form.get('couple_id')

    couple = Couple.query.get(couple_id)
    couple.status = 3
    charter = generate_password_hash(couple_id)
    couple.charter = charter

    db.session.commit()

    results = {}

    results['code'] = 0
    results['msg'] = '批准成功'

    return json.dumps(results)

@admin_bp.route('/reject',methods=['POST'])
def reject():
    couple_id = request.form.get('couple_id')

    couple = Couple.query.get(couple_id)
    couple.status = -1

    db.session.commit()

    results = {}

    results['code'] = 0
    results['msg'] = '操作成功'

    return json.dumps(results)

@admin_bp.route('/access',methods=['GET'])
def access():
    couples = Couple.query.filter_by(status=3).all()

    results = {}
    data = []

    for couple in couples :
        d = {}
        uid = couple.user_id
        user = User.query.get(uid)

        d['name'] = user.real_name
        d['sno']  = user.number

        data.append(d)

    results['code'] = 0
    results['msg'] = '返回成功'
    results['data'] = data

    return json.dumps(results)



