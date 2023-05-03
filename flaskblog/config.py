import os #to setup env variables on personal com
from flask_login import AnonymousUserMixin

class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.account_type = 'Admin'
        self.username = 'test'
        self.email = 'test@gmail.com'
        self.grade = 'Admin'
        self.image_file = 'img'
        self.topics = 'topic'
        self.topics_check = 'y'
        self.id = 1
        
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER') #To update to admin gmail and to use env variable
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    # LOGIN_DISABLED = True #comment out in production