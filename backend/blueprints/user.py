import json

from flask import Blueprint,request,current_app
from flask_login import current_user,login_user,logout_user
from ..models.user import User
from ..extensions import db


user_bp = Blueprint('user',__name__)


@user_bp.route('verify',methods=['POST'])
def verify():
    id = current_user.get_id()
    user = User.query.get(id)

    number = request.form.get('user')
    _password = request.form.get('_password')


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





