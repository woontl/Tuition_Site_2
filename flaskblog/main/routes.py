from flask import render_template, Blueprint, url_for
from flask_login import login_required, current_user
from flaskblog.models import Homework, Question, Working, Note, Activity
import pandas as pd
import datetime as datetime

main = Blueprint('main', __name__) #creating an instance, to be imported

@main.route("/") #Routes are created bring our browers to different pages. "/" represents the root or home page
@main.route("/home") #Both routes bring to the same page
@login_required
def home():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    if current_user.topics:
        topics = current_user.topics.split(',')
        checks = current_user.topics_check.split(',')
    else:
        topics = []
        checks = []
    if current_user.account_type == 'Admin':
        homework = Homework.query.order_by(Homework.date_posted.desc()).first()
        note = Note.query.order_by(Note.date_posted.desc()).first()
        activities = Activity.query.order_by(Activity.date_posted.desc()).all()
    else:
        homework = Homework.query.filter_by(student_id=current_user.id).order_by(Homework.date_posted.desc()).first()
        note = Note.query.filter_by(student_id=current_user.id).order_by(Note.date_posted.desc()).first()
        activities = Activity.query.filter_by(student_id=current_user.id).order_by(Activity.date_posted.desc()).all()
    if homework == None:
        homework = []
        id_arr = []
    else:
        id_arr = [homework.id]
    if note == None:
        note = []
    date_now = datetime.datetime.now()
    activities_date_arr=[]
    for activity in activities:
        activities_date_arr.append(round((date_now-activity.date_posted).total_seconds()/3600))
    pt_arr = []
    question_count_arr = []
    attempt_percentage_arr = []
    correct_percentage_arr = []
    for i in id_arr:
        question_count_arr.append(Question.query.filter_by(homework_id=i).count())
        pt_arr.append(Working.query.filter_by(homework_id=i, point=0).count())
        if Question.query.filter_by(homework_id=i).count() != 0:
            attempt_percentage_arr.append(round((Working.query.filter_by(homework_id=i).count()/Question.query.filter_by(homework_id=i).count())*100,2))
            total_parts = 0
            wrong_parts = 0
            for j in Question.query.filter_by(homework_id=i).all():
                temp = 0
                for k in j.qn_answer.split(';'):
                    if k != "":
                        total_parts += 1
                        temp += 1
                try: 
                    (Working.query.filter_by(question_id=j.id).first()).point
                except:
                    wrong_parts += temp
            for j in Working.query.filter_by(homework_id=i).all():
                wrong_parts += j.point
            correct_percentage_arr.append(round(((total_parts-wrong_parts)/total_parts)*100,2))
        else:
            attempt_percentage_arr.append(0)
            correct_percentage_arr.append(0)
    df = pd.DataFrame({'id': id_arr, 'pt': pt_arr, 'count': question_count_arr, 'attempt_percentage': attempt_percentage_arr, 'correct_percentage': correct_percentage_arr})
    return render_template('home.html', image_file=image_file, homework=homework, note=note, activities=activities, 
                           activities_date_arr=activities_date_arr,df=df, topics=topics, checks=checks) 

@main.route("/about") #Creating a second route
@login_required
def about():
    return render_template('about.html', title='About')