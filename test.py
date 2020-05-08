import requests
import re

from werkzeug.security import check_password_hash,generate_password_hash

headers={"Referer": "http://jwch.fzu.edu.cn/"}

login_url = 'http://59.77.226.32/logincheck.asp'

correct_pattern = '.*id=(.*?)".*'
wrong_pattern = ".*alert\('(.*?)'\);.*"
get_name_pattern = ".*当前用户：(.*?)&nbsp.*"
get_mark_pattern = re.compile(
    '<tr.*?gray;">(.*?)</td>.*?gray;">(.*?)</td>'
    '.*?gray;">(.*?)</td>.*?gray;">(.*?)</td>'
    '.*?gray;">(.*?)</td>.*?gray;">(.*?)</td>'
    ,re.S)

def get_name(muser,passwd):
    data ={}
    data['muser'] = muser
    data['passwd'] = passwd
    results = {}
    session = requests.session()
    response = session.post(url=login_url, data=data, headers=headers)
    response.encoding = response.apparent_encoding

    if len(response.history) == 0 and 'body' not in response.text:
        results['code'] = 1
        results['msg'] = '不存在该用户，请确认是否输入错误，用户名前请不要加字母！！'

    elif 'left.aspx' in response.text:
        id = re.search(correct_pattern, response.text).group(1)
        url = 'http://59.77.226.35/top.aspx?id=' + id
        name = session.get(url=url, headers=headers)
        name = re.search(get_name_pattern, name.text).group(1)

        results['code'] = 0
        results['msg'] = name + '，认证成功！'

    else:
        results['code'] = 1
        results['msg'] = re.search(wrong_pattern, response.text).group(1)

    return results

def get_marks(uid,muser,passwd):
    data = {}
    data['muser'] = muser
    data['passwd'] = passwd

    results = {}
    session = requests.session()
    response = session.post(url=login_url, data=data, headers=headers)
    response.encoding = response.apparent_encoding

    #采用数据库中的数据 进行认证 进行出错判断的原因是防止用户修改了密码而数据库密匙未更新
    if len(response.history) == 0 and 'body' not in response.text:
        results['code'] = 1
        results['msg'] = '不存在该用户，请确认是否输入错误，用户名前请不要加字母！！'

    elif 'left.aspx' in response.text:
        id = re.search(correct_pattern, response.text).group(1)
        scores = []
        url = 'http://59.77.226.35/student/xyzk/cjyl/score_sheet.aspx?id=' + id
        marks =  session.get(url=url, headers=headers)
        mark = re.findall(get_mark_pattern,marks.text)

        for item in mark :
            if '绩点' in item : #正则第一项
                continue
            if item[5] != '':  #本学期修读
                point = float(item[5]) #换算绩点
                if point == 0 or point == 4 : #仅返回不及格和4.0绩点以上科目
                    subject_point = item[4]  #成绩 可能出现同一科不及格和缺考的情况 会造成同一科返回两次
                    if point == 0:
                        subject_point = re.search('<font color=red>(.*?)</font>',item[4])
                        subject_point = subject_point.group(1)
                        if subject_point == '缺考' :  #缺考不返回
                            continue
                    token = str(uid) + item[2] + subject_point
                    score = {
                        'name' : item[2],
                        'point' : subject_point,
                        'token' : generate_password_hash(token)
                    }
                    scores.append(score)
        results['code'] = 0
        results['msg'] = "获取成功"
        results['data'] = scores



    else:
        results['code'] = 1
        results['msg'] = re.search(wrong_pattern, response.text).group(1)

    return results

print(1=='1')