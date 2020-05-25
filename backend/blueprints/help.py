import json
from datetime import datetime

from flask import Blueprint,request,current_app,send_from_directory
from flask_login import current_user,login_user,logout_user
from ..models.help import Help,Order,Comment
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

            if user.is_verify == False and user.is_admin == False:
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
        uid = int(current_user.get_id())
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
        "declaration": help.declaration,
        "release_time": help.release_date.strftime('%Y-%m-%d'),
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
    word = str(request.args.get('word'))

    helps = Help.query.order_by(Help.release_date.desc()).all()


    if word != None :
        words = word.split(' ')
        for i in words :
            for help in helps:
                if i in help.major:
                    if help not in Data :
                        type = 'course'
                        if help.type == True :
                            type = 'skill'

                        d = {
                            "publisher_id": help.user_id,
                            "help_id": help.id,
                            'publisher_nickname' : help.user.nickname,
                            'type' : type,
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

@help_bp.route('/released',methods=['GET'])
def released():
    results = {}
    data = []
    id = int(current_user.get_id())
    #user = User.query.get(id)
    helps = Help.query.filter_by(user_id=id).order_by(Help.release_date.desc()).all()

    for help in helps:
        if help.status == False :
            d = {}
            d['help_id'] = int(help.id)
            d['publisher_name'] = help.user.nickname
            if help.type == True:
                d['type'] = 'skill'
            else :
                d['type'] = 'course'
                d['course_score'] = help.grade

            d['name'] = help.major
            d['declaration'] = help.declaration
            d['release_time'] =help.release_date.strftime('%Y-%m-%d')
            data.append(d)

    results['code'] = 0
    results['msg'] = '查看成功'
    results['data'] = data

    return json.dumps(results)

@help_bp.route('/reserve/<int:id>',methods=['POST'])
@help_bp.route('/<int:id>',methods=['POST'])
def book(id):
    results = {}
    help = Help.query.get(id)
    uid = int(current_user.get_id())
    user = User.query.get(uid)

    #防止重复预约
    if user.orders != None :
        for item in user.orders :
            if item.help_id == id and item.is_pay == False:
                results['code'] = 1
                results['msg'] = '请勿重复预约'
                return json.dumps(results)

    if help.user_id == uid :
        results['code'] = 2
        results['msg'] = '不能预约用户自己发起的辅导！'
        return json.dumps(results)

    if help.status == True :
        results['code'] = 3
        results['msg'] = '该辅导已下架！'

    order = Order(
        date = datetime.today(),
        help_id = id,
        be_user_id = uid,
        help = help,
        be_user = user
    )

    db.session.add(order)
    db.session.commit()

    results['code'] = 0
    results['msg'] = '预约成功'

    return json.dumps(results)


@help_bp.route('/booklist',methods=['GET'])
def booklist():
    results = {}
    data = []
    id = int(current_user.get_id())
    user = User.query.get(id)
    helps = user.helps

    for help in helps:
        d = {}
        d['help_id'] = help.id
        d['name'] = help.major
        orders = help.orders
        book_name = []
        for item in orders :
            if item.state == False :
                dd = {}
                dd['uid'] = item.be_user.id
                dd['nickname'] = item.be_user.nickname
                book_name.append(dd)
        d["book_userlist"] = book_name
        data.append(d)

    results['code'] = 0
    results['msg'] = '查看成功'
    results['data'] = data

    return json.dumps(results)


@help_bp.route('/record',methods=['GET'])
def record():
    results = {}
    data = []

    id = int(current_user.get_id())
    #user = User.query.get(id)
    orders = Order.query.filter_by(be_user_id=id).order_by(Order.date.desc()).all()

    for order in orders:
        help = order.help
        if help!=None and order.state == True:
            type = 'course'
            if type == True:
                type = 'skill'
            d = {
                "help_id" : help.id,
                "publisher_nickname" : help.user.nickname,
                "publisher_id": help.user.id,
                "order_id" : order.id,
                "type" : type,
                "name" : help.major,
                "price" : help.price,
                "release_time" : help.release_date.strftime('%Y-%m-%d'),
                "is_pay" : order.is_pay
            }

            data.append(d)
    results['code'] = 0
    results['msg'] = '查看成功'
    results['data'] = data


    return json.dumps(results)

@help_bp.route('/agree',methods=['POST'])
def agree():
    results = {}
    help_id = request.form.get('help_id')
    user_id = request.form.get('user_id')

    order = Order.query.filter_by(help_id=help_id,be_user_id=user_id).order_by(Order.date.desc()).first()

    order.state = True

    db.session.commit()
    results['code'] = 0
    results['msg'] = '同意预约成功'

    return json.dumps(results)

@help_bp.route('/cancel',methods=['POST'])
def cancel():
    results = {}
    help_id = request.form.get('help_id')
    user_id = int(current_user.get_id())

    order = Order.query.filter_by(help_id=help_id,be_user_id=user_id).order_by(Order.date.desc()).first()

    db.session.delete(order)
    db.session.commit()

    results['code'] = 0
    results['msg'] = '取消预约成功'

    return json.dumps(results)

@help_bp.route('/pay',methods=['POST'])
def pay():
    results = {}
    order_id = request.form.get('order_id')
    order = Order.query.get(order_id)

    order.is_pay = True
    db.session.commit()
    results['code'] = 0
    results['msg'] = '付款成功'

    return json.dumps(results)

@help_bp.route('/remove',methods=['POST'])
def remove():
    results={}
    help_id = request.form.get('help_id')

    help = Help.query.get(help_id)

    uid = int(current_user.get_id())

    if help.user_id == uid:
        help.status = True
        db.session.commit()
        results['code'] = 0
        results['msg'] = '下架成功'

    else :
        results['code'] = -1
        results['msg'] = '非法操作'

    return json.dumps(results)

@help_bp.route('/comment',methods=['POST'])
def comment():
    results = {}

    help_id = request.form.get('help_id')
    text = request.form.get('text')
    star = float(request.form.get('star'))

    user_id = int(current_user.get_id())

    comment = Comment(
        help_id = help_id,
        user_id = user_id,
        text = text,
        date = datetime.today(),
        star = star,
    )

    help = Help.query.get(help_id)
    total = help.user.star * help.user.count + star
    help.user.count += 1
    help.user.star = round(total/help.user.count,1)

    db.session.add(comment)
    db.session.commit()

    results['code'] = 0
    results['msg'] = '评价成功'

    return json.dumps(results)


@help_bp.route('/mycomment',methods=['GET'])
def my_comment():
    results= {}
    data = []
    uid = int(current_user.get_id())
    comments = Comment.query.filter_by(user_id=uid).order_by(Comment.date.desc()).all() #评价人是我的

    if comments != None :
        for comment in comments:
            d = {
                "help_id" : comment.help_id,
                "text" : comment.text,
                "date" : comment.date.strftime('%Y-%m-%d'),
                "publisher_id" : comment.help.user.id,
                "publisher_nickname" : comment.help.user.nickname,
                "name" : comment.help.major
            }
            data.append(d)

    results['code'] = 0
    results['msg'] = '查看成功'
    results['data'] = data

    return json.dumps(results)

@help_bp.route('/index',methods=['GET'])
def index():
    results = {}
    data = []

    page = int(request.args.get('page'))
    each_page = int(request.args.get('each_page'))

    length = Help.query.count()
    pagination = Help.query.order_by(Help.release_date.desc()).paginate(page,per_page=each_page)
    helps = pagination.items

    for help in helps :
        if help.status == False :
            d = {}
            d["publisher_id"] = help.user_id
            d["publisher_nickname"] = help.user.nickname
            d["help_id"] = help.id
            d["name"] = help.major
            d["release_time"] = help.release_date.strftime('%Y-%m-%d')
            d["declaration"] = help.declaration
            if help.type == False:
                d["course_score"] = help.grade
                d['type'] = 'course'
            else :
                d['type'] = 'skill'

            data.append(d)

    results['code'] = 0
    results['msg'] = '返回成功'
    results['data'] = data
    results['length'] = length

    return json.dumps(results)

@help_bp.route('/showcomments',methods=['GET'])
def show_comments():
    results = {}
    data = []
    help_id = request.args.get('help_id')
    #help = Help.query.get(help_id)
    comments = Comment.query.filter_by(help_id=help_id).order_by(Comment.date.desc()).all()
    length = 0

    if comments != None :
        length = len(comments)
        for comment  in comments :
            user = User.query.get(comment.user_id)
            if user == None :
                continue
            else :
                d = {
                    "publisher_id" : comment.user_id,
                    "comment_id" : comment.id,
                    "date" : comment.date.strftime('%Y-%m-%d'),
                    "publisher_nickname" : user.nickname,
                    "text" : comment.text
                }

                data.append(d)

    results['code'] = 0
    results['msg'] = '返回成功'
    results['data'] = data
    results['length'] = length

    return json.dumps(results)

@help_bp.route('/edit',methods=['POST'])
def edit():
    results = {}
    id = request.form.get('help_id')
    declaration = request.form.get('declaration')

    help = Help.query.get(id)

    help.declaration = declaration

    db.session.commit()
    results['code'] = 0
    results['msg'] = '编辑成功'

    return json.dumps(results)






