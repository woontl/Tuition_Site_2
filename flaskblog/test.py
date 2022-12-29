import os
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
MAIL_USERNAME = os.environ.get('EMAIL_USER') #To update to admin gmail and to use env variable
MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

print(SECRET_KEY)
print(SQLALCHEMY_DATABASE_URI)
print(MAIL_PASSWORD)
print(MAIL_USERNAME)