from flask import render_template as real_render_template, Blueprint, flash, redirect, url_for, request, abort, current_app, jsonify, session
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Changelog, Activity, User, Lesson
import datetime as datetime
from flaskblog.lessons.forms import LessonFilterForm, LessonForm, LessonNotesForm
import json

lessons = Blueprint('lessons', __name__) #creating an instance, to be imported

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

# Lesson Routes
@lessons.route("/my_lesson/<string:student>", methods=['GET', 'POST'])
@login_required
def my_lesson(student="ALL"):
    form = LessonFilterForm()
    page = request.args.get('page', 1, type = int)
    if request.method == 'GET' and current_user.account_type == 'Admin':
        users = User.query.filter_by(account_type='User').all()
        users_arr = ['ALL']
        for i in users:
            users_arr.append(i.username)
        form.student.choices = users_arr
        form.student.data = student
        if student == "ALL":
            lessons = Lesson.query.order_by(Lesson.date_posted.desc()).paginate(per_page=5, page=page)
        else:
            user = (User.query.filter_by(username=student).first()).id
            lessons = Lesson.query.filter_by(student_id=user).order_by(Lesson.date_posted.desc()).paginate(per_page=5, page=page)

    elif request.method == 'GET' and current_user.account_type == 'User':
        lessons = Lesson.query.filter_by(student_id=current_user.id).order_by(Lesson.date_posted.desc()).paginate(per_page=5, page=page)

    if request.method == 'POST' and current_user.account_type == 'Admin':
        return redirect(url_for('lessons.my_lesson', student=form.student.data))


    return render_template('my_lesson.html', form=form, lessons=lessons)

@lessons.route("/lesson/new", methods=['GET', 'POST'])
@login_required
def new_lesson():
    form = LessonForm()
    users = User.query.filter_by(account_type='User').all()
    users_arr = []
    for i in users:
        users_arr.append(i.username)
    form.student.choices = users_arr

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.student.data).first()
        if form.title.data == "":
            default_title = form.student.data + ' Lesson ' + str(Lesson.query.filter_by(student_id=user.id).count()+1)
        else:
            default_title = form.title.data
        lesson = Lesson(title=default_title, student_id=user.id, author=current_user)
        db.session.add(lesson)
        activity = Activity(description=default_title+" has been added as lesson!", student_id = user.id, author=current_user)
        db.session.add(activity)
        db.session.commit()
        flash('Your lesson has been created!', 'success')
        return redirect(url_for('lessons.my_lesson', student='ALL'))
    return render_template('create_lesson.html', title='New Lesson', form=form, legend='New Lesson')

@lessons.route("/lesson/<int:lesson_id>", methods=['GET', 'POST']) #route based on lesson id
def lesson(lesson_id):
    session['socketio_code'] = str(lesson_id)
    lesson = Lesson.query.get_or_404(lesson_id) #get data, but return error 404 if not available
    form = LessonNotesForm()
    form.topics.choices = ['topic1', 'topic2']
    if form.validate_on_submit(): #if valid, display all these DB data on webpage
        lesson.notes = form.notes.data
        lesson.formulas = (json.loads(request.form['action']))['ans_merged']
        lesson.topics = form.topics.data
        lesson.workings = form.workings.data
        db.session.commit()
        flash('Your lesson has been updated!', 'success')
        return redirect(url_for('lessons.my_lesson', student = current_user.username)) #redirect back to lesson page after updating
    elif request.method == 'GET':
        if lesson.workings_images:
            workings_images = lesson.workings_images
        else:
            workings_images = ''
        form.workings.data = (lesson.workings)
        session['data'] = lesson.workings
        form.notes.data = lesson.notes
        if lesson.formulas:
            formulas = lesson.formulas.split(';')
        else: 
            formulas = []
        form.topics.data = lesson.topics
    return render_template('lesson.html', lesson=lesson, formulas = formulas, form=form, workings_images=workings_images)

@lessons.route("/lesson/<int:lesson_id>/update", methods=['GET', 'POST']) #route based on lesson id
@login_required
def update_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.author != current_user: #only creator can update lesson
        abort(403)
    form = LessonForm()
    users = User.query.filter_by(account_type='User').all()
    users_arr = []
    for i in users:
        users_arr.append(i.username)
    form.student.choices = users_arr
    if form.validate_on_submit(): #if valid, display all these DB data on webpage
        lesson.title = form.title.data
        lesson.student_id = (User.query.filter_by(username=form.student.data).first()).id
        db.session.commit()
        flash('Your lesson has been updated!', 'success')
        return redirect(url_for('lessons.my_lesson', student="ALL")) #redirect back to lesson page after updating
    elif request.method == 'GET':
        form.title.data = lesson.title
        form.student.data = (User.query.filter_by(id=lesson.student_id).first()).username

    return render_template('create_lesson.html', title='Update Homework', form=form, legend = "Update Homework")

@lessons.route("/lesson/<int:lesson_id>/delete", methods=['GET', 'POST']) #route based on lesson id
@login_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.author != current_user: #only creator can delete lesson
        abort(403)
    date_now = datetime.datetime.now()
    activity = Activity(description=lesson.title+" has been deleted!", student_id = lesson.student_id, 
                        author=current_user, date_posted = date_now)
    db.session.add(activity)
    db.session.delete(lesson)
    db.session.commit()
    flash('Your lesson has been deleted!', 'success')
    return redirect(url_for('lessons.my_lesson', student="ALL"))