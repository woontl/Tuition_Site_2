from flask import render_template as real_render_template, Blueprint, url_for, flash, redirect, request
from flask_login import login_required, current_user
from flaskblog import db
from flaskblog.models import Homework, Question, Working, Activity, Changelog, Bug, Course, Lesson, Exam
from flaskblog.main.forms import ChangelogForm, BugForm
import pandas as pd
import datetime as datetime
from datetime import timedelta

main = Blueprint('main', __name__) #creating an instance, to be imported

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

@main.route("/") 
def landing_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('landing_page.html')
    
@main.route("/home") #Both routes bring to the same page
@login_required
def home():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    if current_user.account_type == 'Admin':
        homework = Homework.query.order_by(Homework.date_posted.desc()).first()
        homework_due_month_calendar = homework.deadline.strftime("%b")
        homework_due_day_calendar = homework.deadline.day
        homework_due = homework.title[:4]
        lesson = Lesson.query.order_by(Lesson.date_posted.desc()).first()
        homework_count = len(Homework.query.all())
        question_count = len(Question.query.all())
        lesson_count = len(Lesson.query.all())
        course_progress = 1
        exam = None
    else:
        homework = Homework.query.filter_by(student_id=current_user.id).order_by(Homework.date_posted.desc()).first()
        if homework:
            homework_due_month_calendar = homework.deadline.strftime("%b")
            homework_due_day_calendar = homework.deadline.day
            homework_due = homework.title[:4]
        else:
            homework_due_month_calendar = ''
            homework_due_day_calendar = ''
            homework_due = ''
        homework_count = len(Homework.query.filter_by(student_id=current_user.id).order_by(Homework.date_posted.desc()).all())
        question_count = 0
        for id in Homework.query.filter_by(student_id=current_user.id).order_by(Homework.date_posted.desc()).all():
            question_count += len(Question.query.filter_by(homework_id=id.id).all())
        lesson = Lesson.query.filter_by(student_id=current_user.id).order_by(Lesson.date_posted.desc()).first()
        lesson_count = len(Lesson.query.filter_by(student_id=current_user.id).order_by(Lesson.date_posted.desc()).all())
        try:
            course_progress = Course.query.filter_by(student_id=current_user.id).first().checked.split(';')
            topics = Course.query.filter_by(student_id=current_user.id).first().topics.split(';')
            total_checks = sum(topic != '' for topic in topics)*4
            checks = sum(int(progress) for progress in (course_progress))
            course_progress = (checks/total_checks)
        except:
            course_progress = 0
        exam = Exam.query.filter_by(student_id=current_user.id).first()
    if exam == None:
        exam_date1 = ''
        exam_date2 = ''
        exam_date3 = ''
        exam_description1 = ''
        exam_description2 = ''
        exam_description3 = ''
    else:
        exam_date1 = exam.date1
        exam_date2 = exam.date2
        exam_date3 = exam.date3
        exam_description1 = exam.description1
        exam_description2 = exam.description2
        exam_description3 = exam.description3
    if homework == None:
        homework = []
        id_arr = []
        homework_num = ''
        homework_title = ''
    else:
        id_arr = [homework.id]
        homework_num = (homework.title.split('-'))[0]
        homework_title = (homework.title.split('-'))[1]
    if lesson == None:
        lesson = []
        lesson_num = ''
        lesson_title = ''
    else:
        lesson_num = (lesson.title.split('-'))[0]
        lesson_title = (lesson.title.split('-'))[1]
    date_now = datetime.datetime.now()
    try:
        homework_due_days = round((homework.deadline - date_now) / timedelta(days=1))
        if homework_due_days < 0:
            homework_due_days = '-'
    except:
        homework_due_days = '-'
    try:
        countdown = abs((exam_date1 - date_now).days)
    except:
        countdown = 0
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
    df = pd.DataFrame({'id': id_arr, 'pt': pt_arr, 'count': question_count_arr, 'attempt_percentage': attempt_percentage_arr,
     'correct_percentage': correct_percentage_arr, 'homework_due_days': homework_due_days})
    return render_template('home.html', image_file=image_file, homework=homework, homework_num = homework_num,
                            homework_title = homework_title, df=df, homework_count=homework_count, question_count=question_count, lesson = lesson, 
                            lesson_num = lesson_num, lesson_title = lesson_title,
                            lesson_count=lesson_count, course_progress=round(course_progress,3),homework_due=homework_due, 
                            homework_due_day_calendar = homework_due_day_calendar, homework_due_month_calendar = homework_due_month_calendar,
                            exam_date1=exam_date1,exam_date2=exam_date2,exam_date3=exam_date3,
                            exam_description1=exam_description1,exam_description2=exam_description2,exam_description3=exam_description3,
                            countdown=countdown)  

@main.route("/activity_readall", methods=['POST']) #Both routes bring to the same page
@login_required
def activity_readall():
    if current_user.account_type == 'Admin':
        activities = Activity.query.all()
    else:
        activities = Activity.query.filter_by(student_id=current_user.id).all()
    for activity in activities:
        activity.read_tag = 1
    db.session.commit()

    # Assuming the previous route is stored in the 'Referer' header of the request
    previous_route = request.headers.get('Referer')
    if previous_route:
        return redirect(previous_route)
    else:
        # Provide a fallback route in case the 'Referer' header is not available
        return redirect(url_for('main.home'))
    # return '', 204

@main.route("/changelog")
@login_required
def changelog():
    page = request.args.get('page', 1, type = int)
    changelogs = Changelog.query.order_by(Changelog.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('changelog.html', changelogs=changelogs)

@main.route("/new_changelog", methods=['GET', 'POST']) #Creating a second route
@login_required
def new_changelog():
    form = ChangelogForm()
    if form.validate_on_submit():
        changelog = Changelog(version=form.version.data, description=form.description.data, author=current_user)
        db.session.add(changelog)
        db.session.commit()
        flash('Your changelog has been created!', 'success')
        return redirect(url_for('main.changelog'))
    return render_template('create_changelog.html', title='New Changelog',
                           form=form, legend='New Changelog')

@main.route("/update_changelog/<int:changelog_id>", methods=['GET', 'POST']) #route based on changelog id
@login_required
def update_changelog(changelog_id):
    changelog = Changelog.query.get_or_404(changelog_id)
    form = ChangelogForm()
    if form.validate_on_submit(): #if valid, display all these DB data on webpage
        changelog.version = form.version.data
        changelog.description = form.description.data
        db.session.commit()
        flash('Your changelog has been updated!', 'success')
        return redirect(url_for('main.changelog'))
    elif request.method == 'GET':
        form.version.data = changelog.version
        form.description.data = changelog.description

    return render_template('create_changelog.html', title='New Changelog',
                           form=form, legend='New Changelog')
    
@main.route("/all_bugs")
@login_required
def all_bugs():
    page = request.args.get('page', 1, type = int)
    if current_user.account_type == 'Admin':
        bugs = Bug.query.order_by(Bug.date_posted.desc()).paginate(per_page=5, page=page)
    else:
        bugs = Bug.query.filter_by(user_id=current_user.id).order_by(Bug.date_posted.desc()).paginate(per_page=5, page=page)
    if bugs == None:
        bugs == []
    return render_template('all_bugs.html', bugs=bugs)

@main.route("/new_bug", methods=['GET', 'POST']) #Creating a second route
@login_required
def new_bug():
    form = BugForm()
    if form.validate_on_submit():
        bug = Bug(issue=form.issue.data, description=form.description.data, status=form.status.data, author=current_user)
        db.session.add(bug)
        db.session.commit()
        flash('Your bug has been added!', 'success')
        return redirect(url_for('main.all_bugs'))
    return render_template('create_bug.html', title='New bug',
                           form=form, legend='New bug')

@main.route("/update_bug/<int:bug_id>", methods=['GET', 'POST']) #route based on bug id
@login_required
def update_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    form = BugForm()
    if form.validate_on_submit(): #if valid, display all these DB data on webpage
        bug.issue = form.issue.data
        bug.description = form.description.data
        bug.status = form.status.data
        db.session.commit()
        flash('Your bug has been updated!', 'success')
        return redirect(url_for('main.all_bugs'))
    elif request.method == 'GET':
        form.issue.data = bug.issue
        form.description.data = bug.description
        form.status.data = bug.status

    return render_template('create_bug.html', title='New bug',
                           form=form, legend='New bug')
