from flask import Blueprint,request
from flask_login import current_user,login_user,logout_user
from ..models.user import User

user_bp = Blueprint('user',__name__)


@user_bp.route('verify',methods=['POST'])
def verify():
    uid = current_user.get_id()
    user = User.get(uid)

    number = request.form.get('user')
    _password = request.form.get('_password')

