from flask import render_template as real_render_template, Blueprint, url_for, flash, redirect, request
from flask_login import login_required, current_user
from flaskblog import db
from flaskblog.models import Homework, Question, Working, Note, Activity, Changelog, Bug
from flaskblog.main.forms import ChangelogForm, BugForm
import pandas as pd
import datetime as datetime

main = Blueprint('main', __name__) #creating an instance, to be imported

def render_template(*args, **kwargs):
    flash('Website has a new version upgrade. Kindly clear your cache!', 'success')
    version = Changelog.query.order_by(Changelog.id.desc()).first()
    if version == None:
        return real_render_template(*args, **kwargs, version='V1.0.0')
    else:
        return real_render_template(*args, **kwargs, version=version.version)

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
    df = pd.DataFrame({'id': id_arr, 'pt': pt_arr, 'count': question_count_arr, 'attempt_percentage': attempt_percentage_arr, 'correct_percentage': correct_percentage_arr})
    return render_template('home.html', image_file=image_file, homework=homework, note=note, activities=activities, 
                           activities_date_arr=activities_date_arr,df=df, topics=topics, checks=checks) 

@main.route("/changelog")
@login_required
def changelog():
    page = request.args.get('page', 1, type = int)
    changelogs = Changelog.query.order_by(Changelog.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('about.html', changelogs=changelogs)

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