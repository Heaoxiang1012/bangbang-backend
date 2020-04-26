# 学长帮帮忙

##### flask initdb 创建数据库

##### 创建一个.env 文件或 .flaskenv 文件 添加 FLASK_APP = backend 
##### 使用发送验证码功能需要在本地 .env文件或.flaskenv 文件 配置邮箱服务、邮箱账号、邮箱密码
##### blueprints\user.py下接口须在登录的情况下测试 否则会报错：object of type 'NoneType' has no len()
##### 获取成绩的token 采用flask 安全模块进行加密 加密字符串由uid+课程名+成绩组成 进行加密 得到密文作为token返回 只需将此token和加密字符串进行check
##### 在根目录新建一个uploads存放用户上传的文件
