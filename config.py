import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig():
    SECRET_KEY = os.getenv('SECRET_KEY','secret string')

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USER_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #ckeditor
    CKEDITOR_FILE_UPLOADER ='main.upload'
    UPLOADED_PATH = os.path.join(basedir,'uploads')
    ALLOW_FILE_EXT = ['jpg','png','jpeg','gif']
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_SERVE_LOCAL=True
    CKEDITOR_HEIGHT=800
    CKEDITOR_ENABLE_CSRF =True
    CKEDITOR_EXTRA_PLUGINS = ['emoji']

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