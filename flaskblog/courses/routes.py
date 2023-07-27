from flask import render_template as real_render_template, Blueprint, flash, redirect, url_for, request, abort, current_app, jsonify, session
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Changelog, Activity, User, Course
import datetime as datetime
from flaskblog.courses.forms import CourseFilterForm
import json

courses = Blueprint('courses', __name__) #creating an instance, to be imported

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

# Courses Routes
@courses.route("/course", methods=['GET', 'POST'])
@login_required
def course():
    form = CourseFilterForm()
    if request.method == 'GET' and current_user.account_type == 'Admin':
        users = User.query.filter_by(account_type='User').all()
        users_arr = []
        for i in users:
            users_arr.append(i.username)
        form.student.choices = users_arr
        math_topics = []
        checked = []
    elif request.method == 'GET':
        try:
            course = Course.query.filter_by(student_id = current_user.id).first()
            math_topics = course.topics.split(';')
            checked = course.checked.split(';')
        except:
            math_topics = []
            checked = []

    if request.method == 'POST':
        if (request.form['action']) != "Load Course":
            topics = ';'.join((json.loads(request.form['action']))['topics'])
            checked = ';'.join(map(str,(json.loads(request.form['action']))['checked']))
            if current_user.account_type == 'Admin':
                user = User.query.filter_by(username = form.student.data).first()
                course = Course.query.filter_by(student_id = user.id).first()
            else:
                course = Course.query.filter_by(student_id = current_user.id).first()
            if course:
                course.topics = topics
                course.checked = checked
                db.session.commit()
            else:
                if current_user.account_type == 'Admin':
                    course = Course(topics=topics, checked=checked, student_id = user.id)
                else:
                    course = Course(topics=topics, checked=checked, student_id = current_user.id)
                db.session.add(course)
                db.session.commit()
            flash('Your course has been saved!', 'success')
            return redirect(url_for('courses.course'))
        else:
            if current_user.account_type == 'Admin':
                user = User.query.filter_by(username = form.student.data).first()
                course = Course.query.filter_by(student_id = user.id).first()
            else:
                course = Course.query.filter_by(student_id = current_user.id).first()
            if course:
                math_topics = course.topics.split(';')
                checked = course.checked.split(';')
            else:
                math_topics = ['New Topic']
                checked = []
            users = User.query.filter_by(account_type='User').all()
            users_arr = []
            for i in users:
                users_arr.append(i.username)
            form.student.choices = users_arr
    return render_template('course.html', math_topics=math_topics, checked=checked, form=form)
