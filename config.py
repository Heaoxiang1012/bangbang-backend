import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig():
    SECRET_KEY = os.getenv('SECRET_KEY','secret string')

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MALI_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOADED_PATH = os.path.join(basedir,'uploads')
    ALLOW_FILE_EXT = ['jpg','png','jpeg','gif']

    #MSG
    CHANGE_PASSWD = ['修改密码成功','原密码错误','密码长度必须在6-16位之间']
    SEND_EMAIL = ['发送成功','email不存在']
    FORGET_PASSWD = ['修改密码成功','email不存在','验证码错误', '密码长度必须在6-16位之间']


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data-dev.db')

class TestConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    DATABASE_HOST = os.getenv('HOST')
    DATABASE_USER = os.getenv('USER')
    DATABASE_PASSWORD = os.getenv('PASSWORD')
    DATABASE = os.getenv('DATABASE')
    DATABASE_CHARSET = 'UTF8'

Config ={
    'development':DevelopmentConfig
}