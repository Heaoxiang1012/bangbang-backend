import re
import json
import os
import uuid

from .models.user import User
from .extensions import mail
from flask_mail import Message


def random_filename(old_filename):
    ext = os.path.splitext(old_filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

def check_register_form(username,password,nickname,email):

    if User.query.filter_by(username=username).first() != None:
       return 1
    elif User.query.filter_by(email=email).first() != None:
        return 2
    elif len(username) > 16 or len(username) < 3 :
        return 3
    elif len(password) > 16 or len(password) < 6 :
        return 4
    elif re.match("^.+@(\\[?)[a-zA-Z0-9\\-\\\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) == None :
        return 5
    elif len(nickname) > 16 or len(nickname) < 3 :
        return 6
    else:
        return 0

def check_requirements(data_json, keys):
    assert type(keys) == list
    try:
        data = json.loads(data_json,strict=False)
        if type(data) == dict and all([i in data for i in keys]):
            return data
    except json.JSONDecodeError:
        pass
    return None

def send_mail(subject,to,body):
    msg = Message(subject,recipients=[to],body=body)
    mail.send(msg)

