import json
from datetime import datetime

from flask import Blueprint,request,current_app,send_from_directory
from flask_login import current_user,login_user,logout_user
from ..models.help import Help
from ..extensions import db
from ..models.user import User
from werkzeug.security import generate_password_hash,check_password_hash


help_bp = Blueprint('help',__name__)

@help_bp.before_request   #!@#!@#
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

@help_bp.route('',methods=['POST'])
def release():
    results = {}

    type = request.form.get('type')
    declaration = request.form.get('declaration')
    price = request.form.get('price')

    help = Help(
        price = price,
        declaration = declaration,
        release_date = datetime.today(),
    )

    if type == 'course' :
        course_token = request.form.get('course_token')
        course = request.form.get('course')
        grade = request.form.get('grade')
        uid = current_user.get_id()
        token = str(uid) + str(course) + str(grade)

        if check_password_hash(course_token,token) == False :
            results['code'] = -1
            results['msg'] = "成绩有误！"

        else :
            help.grade = grade
            help.major = course
            help.user_id = uid
            db.session.add(help)
            db.session.commit()

            data = {
                "id":int(help.id)
            }

            results['code'] = 0
            results['msg'] = '发布成功'
            results['data'] = data

    return json.dumps(results)

@help_bp.route('/<int:id>',methods=['GET'])
def glance(id):
    results = {}
    help = Help.query.get(id)
    type = 'course'

    if help.type == True :
        type = 'skill'

    data = {
        "publisher_id": help.user_id,
        "type": type,
        "name": help.major,
        "price": help.price,
        "declaration": help.declaration
    }

    if help.type == True :
        pass

    else :
        data["course_score"] = help.grade

    results['code'] = 0
    results['msg'] = '查看成功'
    results['data'] = data

    return json.dumps(results)

@help_bp.route('/search',methods=['GET'])
def search():
    results = {}
    Data = []
    data = []
    word = request.args.get('word')
    helps = Help.query.order_by(Help.release_date.desc()).all()


    if word != None :

        for i in word :
            for help in helps:
                if i in help.major:
                    if help not in Data :

                        d = {
                            "publisher_id": help.user_id,
                            'publisher_nickname' : help.user.nickname,
                            'type' : help.type,
                            'name'  : help.major,
                            'price' : help.price,
                            'declaration' : help.declaration,
                        }

                        if help.type == False :
                            d['course_score'] = help.grade

                        Data.append(help)
                        data.append(d)

        results['code'] = 0
        results['msg'] = "查找成功"
        results['data'] = data

    return json.dumps(results)