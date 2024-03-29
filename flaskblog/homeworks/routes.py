from flask import render_template as real_render_template, Blueprint, flash, redirect, url_for, request, abort, current_app, jsonify, session
from flask_login import current_user, login_required
from flaskblog import db, socketio
from flaskblog.models import Homework, Questionbank, Question, Working, User, Activity, Changelog, Lesson, Course
from flaskblog.homeworks.forms import HomeworkForm, QuestionBankForm, QuestionForm, WorkingForm, HomeworkFilterForm
from flaskblog.homeworks.utils import save_qn_picture, save_working_picture ,MQ_formatter
import pandas as pd
import os
import re
import json
from datetime import date, timedelta
import datetime as datetime
from flask_socketio import SocketIO, emit, join_room
from threading import Lock
import operator
from collections import defaultdict
import time
import base64

homeworks = Blueprint('homeworks', __name__) #creating an instance, to be imported

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

# Homework Routes
@homeworks.route("/my_homework/<string:student>", methods=['GET', 'POST'])
@login_required
def my_homework(student="ALL"):
    form = HomeworkFilterForm()
    page = request.args.get('page', 1, type = int)
    if request.method == 'GET' and current_user.account_type == 'Admin':
        users = User.query.filter_by(account_type='User').all()
        users_arr = ['ALL']
        for i in users:
            users_arr.append(i.username)
        form.student.choices = users_arr
        form.student.data = student
        if student == "ALL":
            homeworks = Homework.query.order_by(Homework.date_posted.desc()).paginate(per_page=5, page=page)
            homework_due_days_arr = []
            for homework in homeworks.items:
                date_now = datetime.datetime.now()
                homework_due_days = round((homework.deadline - date_now) / timedelta(days=1))
                if homework_due_days < 0:
                    homework_due_days = '-'
                homework_due_days_arr.append(homework_due_days)
        else:
            user = (User.query.filter_by(username=student).first()).id
            homeworks = Homework.query.filter_by(student_id=user).order_by(Homework.date_posted.desc()).paginate(per_page=5, page=page)
            homework_due_days_arr = []
            for homework in homeworks.items:
                date_now = datetime.datetime.now()
                homework_due_days = round((homework.deadline - date_now) / timedelta(days=1))
                if homework_due_days < 0:
                    homework_due_days = '-'
                homework_due_days_arr.append(homework_due_days)
    elif request.method == 'GET' and current_user.account_type == 'User':
        homeworks = Homework.query.filter_by(student_id=current_user.id).order_by(Homework.date_posted.desc()).paginate(per_page=5, page=page)
        homework_due_days_arr = []
        for homework in homeworks.items:
            date_now = datetime.datetime.now()
            homework_due_days = round((homework.deadline - date_now) / timedelta(days=1))
            if homework_due_days < 0:
                homework_due_days = '-'
            homework_due_days_arr.append(homework_due_days)
    if request.method == 'POST' and current_user.account_type == 'Admin':
        return redirect(url_for('homeworks.my_homework', student=form.student.data))
    id_arr = []
    if homeworks:
        for i in homeworks.items:
            id_arr.append(i.id)
    pt_arr = []
    question_count_arr = []
    attempt_percentage_arr = []
    correct_percentage_arr = []
    for i in id_arr:
        question_count_arr.append(Question.query.filter_by(homework_id=i).count())
        pt_arr.append(Working.query.filter_by(homework_id=i, point=0).count())
        if Question.query.filter_by(homework_id=i).count() != 0:
            attempt_percentage_arr.append(round((Working.query.filter_by(homework_id=i).filter(Working.point != 99).count()/Question.query.filter_by(homework_id=i).count())*100,2))
            total_parts = 0
            wrong_parts = 0
            for j in Question.query.filter_by(homework_id=i).all():
                temp = 0
                for k in j.qn_answer.split(';'):
                    if k != "":
                        total_parts += 1
                        temp += 1
                for l in Working.query.filter_by(question_id=j.id).all():
                    if l.point==99:
                        pass
                    else:
                        wrong_parts += (temp-l.point)
            correct_percentage_arr.append(round(((wrong_parts)/total_parts)*100,2))
        else:
            attempt_percentage_arr.append(0)
            correct_percentage_arr.append(0)
    df = pd.DataFrame({'id': id_arr, 'pt': pt_arr, 'count': question_count_arr, 'attempt_percentage': attempt_percentage_arr, 'correct_percentage': correct_percentage_arr, 'homework_due_days': homework_due_days_arr})
    return render_template('my_homework.html', homeworks=homeworks, df=df, form=form)

@homeworks.route("/homework/new", methods=['GET', 'POST'])
@login_required
def new_homework():
    form = HomeworkForm()
    users = User.query.filter_by(account_type='User').all()
    users_arr = []
    all_topics = []
    all_courses = Course.query.all()
    for course in all_courses:
        topics = course.topics.split(';')
        for topic in topics:
            if topic.strip():
                all_topics.append(topic)
    form.topics.choices = all_topics
    for i in users:
        users_arr.append(i.username)
    if request.method == 'GET':
        form.deadline.data = date.today() + timedelta(days=7)
        form.title.data = 'HW' + ' - '
    form.student.choices = users_arr
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.student.data).first()
        title = (form.title.data).replace('HW', 'HW' + str(Homework.query.filter_by(student_id=user.id).count()+1))
        homework = Homework(title=title, student_id=user.id, deadline=form.deadline.data, topics=form.topics.data,
                             author=current_user)
        db.session.add(homework)
        activity = Activity(description=title+" has been added!", student_id = user.id, author=current_user)
        db.session.add(activity)
        db.session.commit()
        flash('Your homework has been created!', 'success')
        return redirect(url_for('homeworks.my_homework', student='ALL'))
    return render_template('create_homework.html', title='New Homework',
                           form=form, legend='New Homework')

@homeworks.route('/get_topics/<student>', methods=['GET'])
@login_required
def get_topics(student):
    # Logic to retrieve topics based on the selected student
    user = User.query.filter_by(username=student).first()
    course = Course.query.filter_by(student_id=user.id).first()
    try:
        topics = [topic for topic in course.topics.split(';') if topic.strip()]
        return jsonify(topics=topics)
    except:
        return jsonify(topic=[])

@homeworks.route("/homework/<int:homework_id>") #route based on homework id
@login_required
def homework(homework_id):
    homework = Homework.query.get_or_404(homework_id) #get data, but return error 404 if not available
    page = request.args.get('page', 1, type = int)
    questions = Question.query.filter_by(homework_id=homework_id).order_by(Question.id.asc()).paginate(per_page=5, page=page)
    df = pd.read_sql_table('working', db.engine).filter(items=['homework_id','question_id','point'])
    df = df[df["homework_id"]==homework_id].filter(items=['question_id','point'])
    return render_template('homework.html', title=homework.title,homework=homework,homework_id=homework.id, questions=questions, df=df)

@homeworks.route("/homework/<int:homework_id>/update", methods=['GET', 'POST']) #route based on homework id
@login_required
def update_homework(homework_id):
    homework = Homework.query.get_or_404(homework_id)
    if homework.author != current_user: #only creator can update homework
        abort(403)
    form = HomeworkForm()
    users = User.query.filter_by(account_type='User').all()
    users_arr = []
    for i in users:
        users_arr.append(i.username)
    all_topics = []
    all_courses = Course.query.all()
    for course in all_courses:
        topics = course.topics.split(';')
        for topic in topics:
            if topic.strip():
                all_topics.append(topic)
    form.topics.choices = all_topics
    form.student.choices = users_arr
    if form.validate_on_submit(): #if valid, display all these DB data on webpage
        user = User.query.filter_by(username=form.student.data).first()
        homework.title = (form.title.data).replace('HW', 'HW' + str(Homework.query.filter_by(student_id=user.id).count()))
        homework.student_id = (User.query.filter_by(username=form.student.data).first()).id
        homework.deadline = form.deadline.data
        homework.topics = form.topics.data
        db.session.commit()
        flash('Your homework has been updated!', 'success')
        return redirect(url_for('homeworks.my_homework', student="ALL")) #redirect back to homework page after updating
    elif request.method == 'GET':
        form.title.data = homework.title
        form.topics.data = homework.topics
        form.deadline.data = homework.deadline
        form.student.data = (User.query.filter_by(id=homework.student_id).first()).username

    return render_template('create_homework.html', title='Update Homework', form=form, legend = "Update Homework")

@homeworks.route("/homework/<int:homework_id>/delete", methods=['GET', 'POST']) #route based on homework id
@login_required
def delete_homework(homework_id):
    homework = Homework.query.get_or_404(homework_id)
    if homework.author != current_user: #only creator can delete homework
        abort(403)
    date_now = datetime.datetime.now()
    activity = Activity(description=homework.title+" has been deleted!", student_id = homework.student_id, 
                        author=current_user, date_posted = date_now)
    db.session.add(activity)
    delete_q = Question.__table__.delete().where(Question.homework_id == homework_id)
    db.session.execute(delete_q)
    delete_q = Working.__table__.delete().where(Working.homework_id == homework_id)
    db.session.execute(delete_q)
    db.session.delete(homework)
    db.session.commit()
    flash('Your homework has been deleted!', 'success')
    return redirect(url_for('homeworks.my_homework', student="ALL"))

# Questionbank Routes
@homeworks.route("/questionbank/<string:grade>/<string:topics>/<string:difficulty>", methods=['GET', 'POST'])
@login_required
def questionbank(grade="ALL",topics="ALL",difficulty="ALL"):
    page = request.args.get('page', 1, type = int)
    form = QuestionForm()
    all_topics = ['ALL']
    try:
        course = Course.query.filter_by(student_id=current_user.id).first()
        for topic in course.topics.split(';'):
            if topic.strip():
                all_topics.append(topic)
    except:
        all_topics = ['ALL']
    if current_user.account_type == 'Admin':
        courses = Course.query.all()
        for course in courses:
            for topic in course.topics.split(';'):
                if topic.strip():
                    all_topics.append(topic)
    form.topics.choices = all_topics
    images = Questionbank.query.order_by(Questionbank.id.asc()).paginate(per_page=5, page=page)
    if request.method == 'GET':
        form.grade.data = grade
        form.topics.data = topics
        form.difficulty.data = difficulty
        if grade == "ALL":
            grade = "%{}%".format("")
        if topics == "ALL":
            topics = "%{}%".format("")
        else:
            topics = "%{}%".format(topics)
        if difficulty == "ALL":
            difficulty = "%{}%".format("")
        images = Questionbank.query.filter(Questionbank.topics.like(topics),
                                        Questionbank.grade.like(grade),
                                        Questionbank.difficulty.like(difficulty)
                                        ).order_by(Questionbank.id.asc()).paginate(per_page=5, page=page)
        return render_template('questionbank.html', images=images, form=form,legend="Filters")

    if request.method == 'POST':
        topics = "%{}%".format(form.topics.data)
        grade = form.grade.data
        difficulty = form.difficulty.data
        if form.grade.data == "ALL":
            grade = "%{}%".format("")
        if form.topics.data == "ALL":
            topics = "%{}%".format("")
        if form.difficulty.data == "ALL":
            difficulty = "%{}%".format("")
        images = Questionbank.query.filter(Questionbank.topics.like(topics),
                                        Questionbank.grade.like(grade),
                                        Questionbank.difficulty.like(difficulty),
                                        ).order_by(Questionbank.id.asc()).paginate(per_page=5, page=1) #filtered hex list of questions
        return redirect( url_for('homeworks.questionbank', grade=form.grade.data, topics=form.topics.data, difficulty = form.difficulty.data))
        #return render_template('questionbank.html', images=images, form=form,legend="Filters")
    return render_template('questionbank.html', images=images, form=form,legend="Filters")

@homeworks.route("/upload_questionbank", methods=['GET', 'POST'])
@login_required
def upload_questionbank():
    form = QuestionBankForm()
    all_topics = []
    if current_user.account_type == 'Admin':
        courses = Course.query.all()
        for course in courses:
            for topic in course.topics.split(';'):
                if topic.strip():
                    all_topics.append(topic)
    form.topics.choices = all_topics
    if request.method == 'POST':
        if form.img.data == None:
            flash('Please choose image to upload!', 'danger')
            return redirect(url_for('homeworks.upload_questionbank'))
        if form.topics.data == []:
            flash('Please select topics!', 'danger')
            return redirect(url_for('homeworks.upload_questionbank'))
        img = save_qn_picture(form.img.data)
        topics_str = ','.join(form.topics.data)
        ans = (json.loads(request.form['action']))['ans_merged']
        questionbank = Questionbank(grade=form.grade.data, topics=topics_str, img=img,
                                     difficulty=form.difficulty.data, answer=ans)
        db.session.add(questionbank)
        db.session.commit()
        flash('Your question has been added to the Question Bank!', 'success')
        return redirect(url_for('homeworks.upload_questionbank'))
    elif request.method == 'GET':
        return render_template('upload_questionbank.html', title='New Upload', form=form,
                        legend='New Upload')
    
@homeworks.route("/questionbank/<int:questionbank_id>/update", methods=['GET', 'POST'])
@login_required
def update_questionbank(questionbank_id):
    qb = Questionbank.query.get_or_404(questionbank_id)
    form = QuestionBankForm()
    all_topics = []
    if current_user.account_type == 'Admin':
        courses = Course.query.all()
        for course in courses:
            for topic in course.topics.split(';'):
                if topic.strip():
                    all_topics.append(topic)
    form.topics.choices = all_topics
    if request.method == "GET":
        form.grade.data = qb.grade
        form.topics.data = qb.topics
        form.difficulty.data = qb.difficulty
        ans=qb.answer.split(';')
        img_preview = qb.img
        
    elif request.method == "POST":
        qb.grade = form.grade.data
        qb.topics = ','.join(form.topics.data)
        qb.difficulty = form.difficulty.data
        qb.answer = (json.loads(request.form['action']))['ans_merged']
        db.session.commit()
        flash('Your question has been updated in the Question Bank!', 'success')
        
        # Updates all answers in existing Questions
        questions = Question.query.filter_by(questionbank_id=questionbank_id).all()
        for question in questions:
            question.qn_answer = qb.answer
            db.session.commit()
                
        return redirect(url_for('homeworks.questionbank', grade="ALL",topics="ALL",difficulty="ALL"))
    return render_template('upload_questionbank.html', title='Update Questionbank', form=form,
                        legend='Update Questionbank', img_preview=img_preview, ans=ans)

@homeworks.route("/questionbank/<int:questionbank_id>/delete", methods=['GET','POST'])
@login_required
def delete_questionbank(questionbank_id):
    qb = Questionbank.query.get_or_404(questionbank_id)
    os.remove(os.path.join(current_app.root_path,'static/questionbank', qb.img))
    delete_q = Questionbank.__table__.delete().where(Questionbank.id == questionbank_id)
    db.session.execute(delete_q)
    db.session.commit()
    flash('Your question has been deleted from the questionbank!', 'success')
    return redirect(url_for('homeworks.questionbank', grade="ALL",topics="ALL",difficulty="ALL"))

# Question Routes
@homeworks.route("/homework/<int:homework_id>/<int:question_id>/update/<string:grade>/<string:topics>/<string:difficulty>/<string:load>", methods=['GET', 'POST']) #route based on homework id
@login_required
def update_question(homework_id, question_id, grade="ALL",topics="ALL",difficulty="ALL", load="not_loaded"):
    question = Question.query.get_or_404(question_id)
    homework = Homework.query.get_or_404(homework_id)
    page = request.args.get('page', 1, type = int)
    form = QuestionForm()
    all_topics = []
    if current_user.account_type == 'Admin':
        courses = Course.query.all()
        for course in courses:
            for topic in course.topics.split(';'):
                if topic.strip():
                    all_topics.append(topic)
    form.topics.choices = all_topics
    if request.method == 'GET':
        if load == "not_loaded" :
            form.grade.data = question.grade
            form.topics.data = question.topics
            form.difficulty.data = question.difficulty
            form.title.data = question.title
            images = Questionbank.query.filter(Questionbank.img==question.qn_img).paginate(per_page=1, page=1)
            return render_template('update_question.html',question_id=question_id,homework_id=homework.id,images=images,title='Update Question', load="not_loaded", form=form, legend = "Update Question")
        else:
            form.grade.data = grade
            form.topics.data = topics
            form.difficulty.data = difficulty
            form.title.data = question.title
            if form.grade.data == "ALL":
                grade = "%{}%".format("")
            if form.topics.data == "ALL":
                topics = "%{}%".format("")
            else:
                topics = "%{}%".format(topics)
            if form.difficulty.data == "ALL":
                difficulty = "%{}%".format("")
            images = Questionbank.query.filter(Questionbank.grade.like(grade),
                                        Questionbank.difficulty.like(difficulty),
                                        Questionbank.topics.like(topics)).paginate(per_page=5, page=page)
            return render_template('update_question.html',question_id=question_id,homework_id=homework.id,images=images,title='Update Question', load="loaded",form=form, legend = "Update Question")

    if request.method == 'POST':
        try:
            if (request.form['action']) != "Load Questions":
                img_id = (request.form['action'])
                qb = Questionbank.query.filter(Questionbank.id==img_id).first()
                if qb is None:
                    qb = Questionbank.query.filter(Questionbank.img==question.qn_img).first()
                    question.qn_img = qb.img
                else:
                    question.qn_img = qb.img
                question.title = form.title.data
                question.grade = qb.grade
                question.topics = qb.topics
                question.difficulty = qb.difficulty
                question.questionbank_id = qb.id
                question.qn_answer=qb.answer
                db.session.commit()
                flash('Your question has been updated!', 'success')
                return redirect(url_for('homeworks.homework', homework_id=homework.id))      
            else:
                grade = form.grade.data
                topics = form.topics.data
                difficulty = form.difficulty.data
                if form.grade.data == "ALL":
                    grade = "%{}%".format("")
                if form.topics.data == "ALL":
                    topics = "%{}%".format("")
                else:
                    topics = "%{}%".format(topics)
                if form.difficulty.data == "ALL":
                    difficulty = "%{}%".format("")
                images = Questionbank.query.filter(Questionbank.grade.like(grade),
                                            Questionbank.difficulty.like(difficulty),
                                            Questionbank.topics.like(topics)).paginate(per_page=5, page=1)
                return render_template('update_question.html', title='Update Question', question_id=question_id, homework_id=homework.id, load="loaded" ,form=form, images=images, legend = "Update Question")
        except:
            pass

@homeworks.route("/homework/<int:homework_id>/<int:question_id>/delete", methods=['GET', 'POST']) #route based on homework id
@login_required
def delete_question(homework_id,question_id):
    homework = Homework.query.get_or_404(homework_id)
    if homework.author != current_user: #only creator can delete homework
        abort(403)
    delete_q = Question.__table__.delete().where(Question.id == question_id and Question.homework_id == homework_id)
    db.session.execute(delete_q)
    delete_w = Working.__table__.delete().where(Working.question_id == question_id and Working.homework_id == homework_id)
    db.session.execute(delete_w)
    db.session.commit()
    
    count = 1
    for question in Question.query.filter(Question.homework_id==homework_id).all():
        question.title = 'Question ' + str(count)
        count += 1
    db.session.commit()
    flash('Your question has been deleted!', 'success')
    return redirect(url_for('homeworks.homework',homework_id=homework.id))

@homeworks.route("/homework/<int:homework_id>/new_question/<string:grade>/<string:topics>/<string:difficulty>", methods=['GET', 'POST'])
@login_required
def new_question(homework_id, grade="ALL",topics="ALL",difficulty="ALL"):
    page = request.args.get('page', 1, type = int)
    homework = Homework.query.get_or_404(homework_id)
    if homework.author != current_user: #only creator can add qn to HW
        abort(403)
    form = QuestionForm()
    all_topics = ['ALL']
    if current_user.account_type == 'Admin':
        courses = Course.query.all()
        for course in courses:
            for topic in course.topics.split(';'):
                if topic.strip():
                    all_topics.append(topic)
    form.topics.choices = all_topics
    images = Questionbank.query.order_by(Questionbank.id.asc()).paginate(per_page=5, page=page)
    if request.method == 'GET':
        form.grade.data = grade
        form.topics.data = topics
        form.difficulty.data = difficulty
        if form.grade.data == "ALL":
            grade = "%{}%".format("")
        if form.topics.data == "ALL":
            topics = "%{}%".format("")
        else:
            topics = "%{}%".format(topics)
        if form.difficulty.data == "ALL":
            difficulty = "%{}%".format("")
        images = Questionbank.query.filter(Questionbank.grade.like(grade),
                                    Questionbank.difficulty.like(difficulty),
                                    Questionbank.topics.like(topics)).paginate(per_page=5, page=page)
        return render_template('new_question.html',homework_id=homework.id,images=images,title='New Question', form=form, legend = "New Question")
    
    if request.method == 'POST':
        if (request.form['action']) != "Load Questions":
            img_id = (request.form['action'])
            qb = Questionbank.query.filter(Questionbank.id==img_id).first()
            if qb is None:
                flash('Please select your question before submitting!', 'danger')
                return redirect(url_for('homeworks.new_question',homework_id=homework.id, grade=form.grade.data, topics=form.topics.data, difficulty = form.difficulty.data)) #redirect back to homework page after updating
            if form.title.data == "":
                default_title = 'Question ' + str(Question.query.filter_by(homework_id=homework.id).count() + 1)
            else:
                default_title = form.title.data
            question = Question(title=default_title, questionbank_id=qb.id, homework_id=homework_id, grade=qb.grade, qn_img=qb.img, qn_answer=qb.answer,
                             topics=qb.topics, difficulty=qb.difficulty)
            db.session.add(question)
            
            # Add blank entry to Workings 
            final_ans = ';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;'
            right_wrong = 'NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW;NEW'
            question_id = Question.query.order_by(Question.id.desc()).first().id
            working = Working(workings='[]', workings3='[]', final_ans=final_ans, homework_id=homework_id, question_id=question_id, point=99,right_wrong=right_wrong)
            db.session.add(working)
            db.session.commit()
            
            flash('Your question has been added!', 'success')
            return redirect(url_for('homeworks.new_question',homework_id=homework.id, grade=form.grade.data, topics=form.topics.data, difficulty = form.difficulty.data, page=page)) #redirect back to homework page after updating
        grade = form.grade.data
        topics = form.topics.data
        difficulty = form.difficulty.data
        if form.grade.data == "ALL":
            grade = "%{}%".format("")
        if form.topics.data == "ALL":
            topics = "%{}%".format("")
        else:
            topics = "%{}%".format(topics)
        if form.difficulty.data == "ALL":
            difficulty = "%{}%".format("")
        images = Questionbank.query.filter(Questionbank.grade.like(grade),
                                    Questionbank.difficulty.like(difficulty),
                                    Questionbank.topics.like(topics)).paginate(per_page=5, page=1)
        return redirect(url_for('homeworks.new_question',homework_id=homework.id, grade=form.grade.data, topics=form.topics.data, difficulty = form.difficulty.data)) #redirect back to homework page after updating
    return render_template('new_question.html', images=images, homework_id=homework_id, title='New Question', form=form, legend = "New Question")

@homeworks.route("/homework/<int:homework_id>/<int:question_id>/solve", methods=['GET', 'POST']) #route based on homework id
@login_required
def solve_question(homework_id, question_id):
    session['socketio_code'] = str(homework_id) + '/' + str(question_id)
    homework = Homework.query.get_or_404(homework_id)
    working = Working.query.filter(Working.homework_id==homework_id, Working.question_id==question_id).first()
    form = WorkingForm()
    question = Question.query.filter(Question.id==question_id, Question.homework_id==homework_id).first()
    correct_ans = re.sub('【(.*?)】','\\\\MathQuillMathField{}',question.qn_answer).split(';')
    check_ans = MQ_formatter(question.qn_answer).split(';')
    if request.method == 'GET':
        form.workings.data = (working.workings)
        session['data'] = working.workings
        final_ans = working.final_ans.split(';')
        right_wrong = working.right_wrong.split(';')
        if working.workings_images:
            workings_images = working.workings_images
        else:
            workings_images = ''
    elif request.method == 'POST':
        working = Working.query.filter(Working.homework_id==homework_id, Working.question_id==question_id).first()
        final_ans = MQ_formatter(request.form['action'])
        point = []
        for i,j in zip((final_ans.split(';')),(check_ans)):
            if i == j:
                point.append(0)
            else:
                point.append(1)
        right_wrong = ';'.join(map(str,point))
        final_ans = (request.form['action'])
        working.final_ans = final_ans
        working.point = sum(point)
        working.right_wrong = right_wrong
        date_now = datetime.datetime.now()
        activity = Activity(description=question.title+ " has been attempted in "+homework.title+"!", student_id = homework.student_id, 
                            author=current_user, date_posted = date_now)
        db.session.add(activity)
        db.session.commit()
        if sum(point) != 0:
            flash('Your answer is wrong!', 'danger')
            return redirect(url_for('homeworks.solve_question', homework_id=homework.id, question_id=question.id))
        else:
            flash('Your answer is correct!', 'success')
            return redirect(url_for('homeworks.homework', homework_id=homework.id))
    return render_template('working.html', title='Solve Question', form=form, legend = "Solve Question", question=question, ans=correct_ans, 
                           final_ans=final_ans, right_wrong=right_wrong, check_ans=check_ans, homework_id=homework_id, question_id=question_id, 
                           workings_images = workings_images)

# @socketio.on('save')
def auto_save_canvas(data):
    match = re.match(r'(\d+)/(\d+)', session['socketio_code'])
    if match:
        homework_id = int(match.group(1))
        question_id = int(match.group(2))
        working = Working.query.filter(Working.homework_id==homework_id, Working.question_id==question_id).first()
        existing_list = json.loads(working.workings)
        if data == 'clear':
            working.workings = '[]'
        elif data == 'undo':
            existing_list.pop()
            working.workings = json.dumps(existing_list)
        else:
            existing_list.append(data['data'])
            working.workings = json.dumps(existing_list)
        db.session.commit()
    else:
        lesson_id = session['socketio_code']
        lesson = Lesson.query.filter(Lesson.id==lesson_id).first()
        existing_list = json.loads(lesson.workings)
        if data == 'clear':
            lesson.workings = '[]'
        elif data == 'undo':
            existing_list.pop()
            lesson.workings = json.dumps(existing_list)
        else:
            existing_list.append(data['data'])
            lesson.workings = json.dumps(existing_list)
        db.session.commit()
    # match = re.match(r'(\d+)/(\d+)', session['socketio_code'])
    # if match:
    #     homework_id = int(match.group(1))
    #     question_id = int(match.group(2))
    #     working = Working.query.filter(Working.homework_id==homework_id, Working.question_id==question_id).first()
    #     working.workings = data
    #     db.session.commit()
    # else:
    #     lesson_id = session['socketio_code']
    #     lesson = Lesson.query.filter(Lesson.id==lesson_id).first()
    #     lesson.workings = data
    #     db.session.commit()

@socketio.on('save_images')
def auto_save_canvas_images(data):
    match = re.match(r'(\d+)/(\d+)', session['socketio_code'])
    if match:
        homework_id = int(match.group(1))
        question_id = int(match.group(2))
        working = Working.query.filter(Working.homework_id==homework_id, Working.question_id==question_id).first()
        img_png = save_working_picture(data)
        image_data = json.loads(data)
        image_data['dataURL'] = img_png
        modified_json_string = json.dumps(image_data)
        if working.workings_images:
            working.workings_images += '@@@'+ modified_json_string
        else:
            working.workings_images = modified_json_string
        db.session.commit()
        emit('load_images', working.workings_images , broadcast=True, include_self=False, to=session['socketio_code'])
    else:
        lesson_id = session['socketio_code']
        lesson = Lesson.query.filter(Lesson.id==lesson_id).first()
        img_png = save_working_picture(data)
        image_data = json.loads(data)
        image_data['dataURL'] = img_png
        modified_json_string = json.dumps(image_data)
        if lesson.workings_images:
            lesson.workings_images += '@@@'+ modified_json_string
        else:
            lesson.workings_images = modified_json_string
        db.session.commit()
        emit('load_images', lesson.workings_images , broadcast=True, include_self=False, to=session['socketio_code'])

@socketio.on('connect')
def socket_connect():
    join_room(session['socketio_code'])

@socketio.on('stroke')
def stroke(data):
    join_room(session['socketio_code'])
    emit('stroke', data, broadcast=True, include_self=False, to=session['socketio_code'])
    # emit('save', broadcast=False, include_self=True, to=session['socketio_code'])
    auto_save_canvas(data)

@socketio.on('strokes')
def strokes(data):
    join_room(session['socketio_code'])
    emit('strokes', data, broadcast=True, include_self=False, to=session['socketio_code'])

@socketio.on('delete')
def delete(data):
    join_room(session['socketio_code'])
    emit('delete', data, broadcast=True, include_self=False, to=session['socketio_code'])
    # emit('save', broadcast=False, include_self=True, to=session['socketio_code'])
    auto_save_canvas('undo')

@socketio.on('clear')
def clear():
    join_room(session['socketio_code'])
    emit('clear', broadcast=True, include_self=False, to=session['socketio_code'])
    # emit('save', broadcast=False, include_self=True, to=session['socketio_code'])
    auto_save_canvas('clear')