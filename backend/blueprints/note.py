import json
import os
from datetime import datetime

from flask import Blueprint,request,current_app,send_from_directory
from flask_login import current_user,login_user,logout_user
from ..models.note import Note,File
from ..extensions import db
from ..models.user import User
from ..utils import random_filename


note_bp = Blueprint('note',__name__)

@note_bp.before_request   #!@#!@#
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

            if user.is_verify == False:
                result['code'] = -2
                result['msg'] = '请先实名制认证！'
                return json.dumps(result)

@note_bp.route('',methods=['POST'])
def release():
    results = {}
    data = {}
    title = request.form.get('title')
    tag = request.form.get('tag')
    content = request.form.get('content')

    uid = current_user.get_id()

    note = Note(
        title = title,
        tag = tag,
        content = content,
        note_date = datetime.today(),
        user_id = uid
    )

    db.session.add(note)
    db.session.commit()

    data['id'] = note.id
    results['code'] = 0
    results['msg'] = '发布成功'
    results['data'] = data

    return json.dumps(results)

@note_bp.route('/published',methods=['GET'])
def my_published():
    results = {}
    data = []
    id = current_user.get_id()
    user  = User.query.get(id)

    if user.notes != None :
        for item in user.notes:
            d = {
                "note_id" : item.id,
                "title" : item.title,
                "tag" : item.tag,
                "content" : item.content,
            }
            data.append(d)

    results['code'] = 0
    results['msg'] = 'success'
    results['data'] = data

    return json.dumps(results)

@note_bp.route('/search',methods=['GET'])
def search():
    results = {}
    Data = []
    data = []
    word = str(request.args.get('word'))

    notes = Note.query.order_by(Note.note_date.desc()).all()

    if word != None:
        words = word.split(' ')
        for i in words:
            for note in notes:
                if i in note.tag:
                    if note not in Data:

                        d = {
                            "publisher_id": note.user_id,
                            'publisher_nickname': note.user.nickname,
                            'note_id' : note.id,
                            'title': note.title,
                            'tag': note.tag,
                            'content': note.content,
                            "note_date": note.note_date.strftime('%Y-%m-%d'),
                        }

                        Data.append(note)
                        data.append(d)

        results['code'] = 0
        results['msg'] = "查找成功"
        results['data'] = data

    return json.dumps(results)

@note_bp.route('/<int:id>',methods=['GET'])
def note(id):
    results = {}
    note = Note.query.get(id)

    data = {
        "publisher_id" : note.user_id,
        "title" : note.title,
        "tag" : note.tag,
        "content" : note.content,
        "note_date" :note.note_date.strftime('%Y-%m-%d')
    }

    results['code'] = 0
    results['msg'] = '查看成功'
    results['data'] = data

    return json.dumps(results)

@note_bp.route('/upload',methods=['POST'])
def upload():
    results = {}
    f = request.files.get('file')

    filename = random_filename(f.filename)

    f.save(os.path.join(current_app.config['FILE_PATH'], filename))

    file = File(
        filename=filename
    )

    db.session.add(file)
    db.session.commit()

    data = {
        "file_id":file.id
    }

    results['code'] = 0
    results['msg'] = '上传成功'
    results['data'] = data

    return json.dumps(results)

@note_bp.route('/file/<int:id>',methods=['GET'])
def get_file(id):
    file = File.query.get(id)
    filename = file.filename

    return send_from_directory(current_app.config['FILE_PATH'], filename)

@note_bp.route('/categories',methods=['GET'])
def categories():
    results = {}
    data = []
    notes = Note.query.all()
    for note in notes :
        if note.tag not in data:
            data.append(note.tag)

    results['code'] = 0
    results['msg'] = 'success'
    results['data'] = data

    return json.dumps(results)

@note_bp.route('/index',methods=['GET'])
def index():
    results={}
    data = []

    tag = request.args.get('tag')
    page = int(request.args.get('page'))
    each_page = int(request.args.get('each_page'))

    length = Note.query.filter_by(tag=tag).count()
    pagination = Note.query.filter_by(tag=tag).order_by(Note.note_date.desc()).paginate(page,per_page=each_page)
    notes = pagination.items

    for note in notes :
        d = {}
        d["publisher_id"] = note.user_id
        d["publisher_nickname"] = note.user.nickname
        d["note_id"] = note.id
        d["title"] = note.title
        d["content"] = note.content[0:32] +'...'
        d["note_date"] = note.note_date.strftime('%Y-%m-%d')
        d["compliments"] = note.compliments

        data.append(d)

    results['code'] = 0
    results['msg'] = '返回成功'
    results['data'] = data
    results['length'] = length

    return json.dumps(results)

@note_bp.route('/edit',methods=['POST'])
def edit():
    results = {}
    id = request.form.get('note_id')
    content = request.form.get('content')

    note = Note.query.get(id)
    note.content = content
    note.note_date = datetime.today()

    db.session.commit()

    results['code'] = 0
    results['msg'] = '修改成功'

    return json.dumps(results)

