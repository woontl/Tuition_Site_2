from datetime import datetime
from enum import unique
from re import T
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): #Creating user table in DB
    id = db.Column(db.Integer, primary_key = True) #ID defined as an integer and to be the primary key)
    username = db.Column(db.String(20), unique=True, nullable=False) #name to be a string, max 20 characters, must be unique, and required, cannot be null
    email = db.Column(db.String(120), unique=True, nullable=False) 
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') #user image defaults to a default.jpg
    password = db.Column(db.String(60), nullable=False)
    account_type = db.Column(db.String(60), nullable=False)
    notes = db.relationship('Note', backref='author', lazy=True)
    homeworks = db.relationship('Homework', backref='author', lazy=True)
    activities = db.relationship('Activity', backref='author', lazy=True)
    changelogs = db.relationship('Changelog', backref='author', lazy=True)
    bugs = db.relationship('Bug', backref='author', lazy=True)
    topics = db.Column(db.String(1000))
    topics_check = db.Column(db.String(1000))
    description1 = db.Column(db.String(1000))
    date1 = db.Column(db.Date)
    time1 = db.Column(db.Time)
    description2 = db.Column(db.String(1000))
    date2 = db.Column(db.Date)
    time2 = db.Column(db.Time)
    description3 = db.Column(db.String(1000))
    date3 = db.Column(db.Date)
    time3 = db.Column(db.Time)
    description4 = db.Column(db.String(1000))
    date4 = db.Column(db.Date)
    time4 = db.Column(db.Time)
    grade = db.Column(db.String(200))

    def get_reset_token(self, expires_sec=1800): #Token expires in 1800 secs
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod #for functions without 'self' declaration
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.image_file}')" #returns details of user created

class Homework(db.Model): #Creating homework table in DB
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False, default = datetime.now)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #foreign key links to User table
    questions = db.relationship('Question', backref='hwk', lazy=True)
    workings = db.relationship('Working', backref='hwk', lazy=True)

    def __repr__(self):
        return f"Homework('{self.title}', '{self.date_posted}')"

class Questionbank(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    img = db.Column(db.Text, unique=True, nullable=False)
    grade = db.Column(db.String(200), nullable=False)
    tags = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    checked = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.now)

    def __repr__(self):
        return f"Questionbank('{self.grade}', '{self.tags}')"

class TagsList(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tag = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"TagsList('{self.id}', '{self.tag}')"
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'), nullable=False)
    questionbank_id = db.Column(db.Integer, db.ForeignKey('questionbank.id'), nullable=False)
    grade = db.Column(db.String(200), nullable=False)
    tags = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.String(200), nullable=False)
    qn_img = db.Column(db.Text, nullable=False)
    qn_answer = db.Column(db.String(200), nullable=False)
    checked = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Question('{self.id}', '{self.title}')"

class Working(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    homework_id = db.Column(db.Integer, db.ForeignKey('homework.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    workings = db.Column(db.Text)
    workings2 = db.Column(db.Text)
    workings3 = db.Column(db.Text)
    final_ans = db.Column(db.Text, nullable=False)
    point = db.Column(db.Integer)
    right_wrong = db.Column(db.String(200))

    def __repr__(self):
        return f"Working('{self.id}')"

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    workings = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #foreign key links to User table

    def __repr__(self):
        return f"Note('{self.id}')"
    
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(1000), nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #foreign key links to User table

    def __repr__(self):
        return f"Activity('{self.id}')"
    
class Changelog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    version = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.now)
    description = db.Column(db.String(99999), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #foreign key links to User table
    
    def __repr__(self):
        return f"Changelog('{self.id}')"
    
class Bug(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    issue = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.now)
    description = db.Column(db.String(99999), nullable=False)
    status = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #foreign key links to User table
    
    def __repr__(self):
        return f"Bug('{self.id}')"