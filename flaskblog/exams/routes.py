from flask import render_template as real_render_template, Blueprint, flash, redirect, url_for, request, abort, current_app, jsonify, session
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Changelog, Activity, User, Exam
import datetime as datetime
from flaskblog.exams.forms import ExamsForm
import json

exams = Blueprint('exams', __name__) #creating an instance, to be imported

def render_template(*args, **kwargs):
    try:
        dark_mode = current_user.dark_mode
    except:
        dark_mode = 'On'
    version = Changelog.query.order_by(Changelog.id.desc()).first()
    if current_user.account_type == 'Admin':
        activities = Activity.query.order_by(Activity.date_posted.desc()).limit(5).all()
    else:
        activities = Activity.query.filter_by(student_id=current_user.id).order_by(Activity.date_posted.desc()).limit(5).all()
    date_now = datetime.datetime.now()
    activities_date_arr=[]
    for activity in activities:
        activities_date_arr.append(round((date_now-activity.date_posted).total_seconds()/3600/24))
    if version == None:
        return real_render_template(*args, **kwargs, version='V1.0.0', dark_mode=dark_mode, activities=activities, 
                           activities_date_arr=activities_date_arr)
    else:
        return real_render_template(*args, **kwargs, version=version.version, dark_mode=dark_mode, activities=activities, 
                           activities_date_arr=activities_date_arr)

# Exams Routes
@exams.route("/exam", methods=['GET', 'POST'])
@login_required
def exam():
    form = ExamsForm()
    date1=''
    date2=''
    date3=''
    if request.method == 'GET' and current_user.account_type == 'Admin':
        users = User.query.filter_by(account_type='User').all()
        users_arr = []
        for i in users:
            users_arr.append(i.username)
        form.student.choices = users_arr
    elif request.method == 'GET':
        try:
            exam = Exam.query.filter_by(student_id = current_user.id).first()
            date1=exam.date1
            form.description1.data=exam.description1
            date2=exam.date2
            form.description2.data=exam.description2
            date3=exam.date3
            form.description3.data=exam.description3
        except:
            pass

    if request.method == 'POST':
        if (request.form['action']) != "Load Exams":
            if current_user.account_type == 'Admin':
                user = User.query.filter_by(username = form.student.data).first()
                exam = Exam.query.filter_by(student_id = user.id).first()
            else:
                exam = Exam.query.filter_by(student_id = current_user.id).first()
            if exam:
                exam.date1 = form.date1.data
                exam.description1 = form.description1.data
                exam.date2 = form.date2.data
                exam.description2 = form.description2.data
                exam.date3 = form.date3.data
                exam.description3 = form.description3.data
                db.session.commit()
            else:
                if current_user.account_type == 'Admin':
                    exam = Exam(student_id = user.id, date1=form.date1.data, description1=form.description1.data,
                                                                date2=form.date2.data, description2=form.description2.data,
                                                                date3=form.date3.data, description3=form.description3.data)
                else:
                    exam = Exam(student_id = current_user.id, date1=form.date1.data, description1=form.description1.data,
                                                                date2=form.date2.data, description2=form.description2.data,
                                                                date3=form.date3.data, description3=form.description3.data)
                db.session.add(exam)
                db.session.commit()
            flash('Your exam has been saved!', 'success')
            return redirect(url_for('exams.exam'))
        else:
            users = User.query.filter_by(account_type='User').all()
            users_arr = []
            for i in users:
                users_arr.append(i.username)
            form.student.choices = users_arr
            if current_user.account_type == 'Admin':
                user = User.query.filter_by(username = form.student.data).first()
                exam = Exam.query.filter_by(student_id = user.id).first()
            else:
                exam = Exam.query.filter_by(student_id = current_user.id).first()
            if exam:
                form.description1.data=exam.description1
                date2 = exam.date2
                form.description2.data=exam.description2
                date3 = exam.date3
                form.description3.data=exam.description3
                date1 = exam.date1
            else:
                form.date1.data=''
                form.description1.data=''
                form.date2.data=''
                form.description2.data=''
                form.date3.data=''
                form.description3.data=''
    return render_template('exam.html', form=form, date1=date1, date2=date2, date3=date3)
