from flask import render_template as real_render_template, Blueprint, flash, redirect, url_for, request, abort, current_app
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import User, Note, Activity, Changelog
from flaskblog.notes.forms import NotesFilterForm, NoteForm
import pandas as pd
import datetime as datetime

notes = Blueprint('notes', __name__) #creating an instance, to be imported

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


@notes.route("/notes_all/<string:student>", methods=['GET', 'POST'])
@login_required
def notes_all(student="ALL"):
    form = NotesFilterForm()
    page = request.args.get('page', 1, type = int)
    if request.method == 'GET' and current_user.account_type == 'Admin':
        users = User.query.filter_by(account_type='User').all()
        users_arr = ['ALL']
        for i in users:
            users_arr.append(i.username)
        form.student.choices = users_arr
        form.student.data = student
        if student == "ALL":
            notes = Note.query.order_by(Note.date_posted.desc()).paginate(per_page=5, page=page)
        else:
            user = (User.query.filter_by(username=student).first()).id
            notes = Note.query.filter_by(student_id=user).order_by(Note.date_posted.desc()).paginate(per_page=5, page=page)
    elif request.method == 'GET' and current_user.account_type == 'User':
        notes = Note.query.filter_by(student_id=current_user.id).order_by(Note.date_posted.desc()).paginate(per_page=5, page=page)
    if request.method == 'POST' and current_user.account_type == 'Admin':
        return redirect(url_for('notes.notes_all', student=form.student.data))
    date_now = datetime.datetime.now().strftime("%Y-%m-%d")
    return render_template('notes_all.html', form=form, legend="Filters", notes=notes, date_now=date_now)

@notes.route("/notes/new", methods=['GET', 'POST'])
@login_required
def new_note():
    form = NoteForm()
    users = User.query.filter_by(account_type='User').all()
    users_arr = []
    for i in users:
        users_arr.append(i.username)
    form.student.choices = users_arr
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.student.data).first()
        if form.title.data == "":
            default_title = form.student.data + ' Note ' + str(Note.query.filter_by(student_id=user.id).count()+1)
        else:
            default_title = form.title.data
        note = Note(title=default_title, student_id=user.id, author=current_user)
        date_now = datetime.datetime.now()
        activity = Activity(description=default_title+ " has been added in Notes!", student_id = note.student_id, 
                            author=current_user, date_posted = date_now)
        db.session.add(activity)
        db.session.add(note)
        db.session.commit()
        flash('Your note has been created!', 'success')
        return redirect(url_for('notes.notes_all', student='ALL'))
    return render_template('create_note.html', title='New Note',
                           form=form, legend='New Note')
    
@notes.route("/notes/<int:note_id>", methods=['GET', 'POST'])
def note(note_id):
    note = Note.query.get_or_404(note_id) #get data, but return error 404 if not available
    form = NoteForm()
    if request.method == 'GET':
        form.workings.data = note.workings
    elif request.method == 'POST':
        try:
            if request.form['refresh'] == "refresh":
                form.workings.data = note.workings
            if request.form['refresh'] == "save":
                note.workings = form.workings.data
                flash('Your note has been saved!', 'success')
                db.session.commit()
            return redirect(url_for('notes.all_notes', student='ALL'))
        except:
            pass
    return render_template('note.html', title=note.title,note=note,note_id=note.id, form=form)

@notes.route("/notes/<int:note_id>/update", methods=['GET', 'POST']) #route based on note id
@login_required
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    form = NoteForm()
    users = User.query.filter_by(account_type='User').all()
    users_arr = []
    for i in users:
        users_arr.append(i.username)
    form.student.choices = users_arr
    if form.validate_on_submit(): #if valid, display all these DB data on webpage
        user = User.query.filter_by(username=form.student.data).first()
        note.title = form.title.data
        if form.title.data == "":
            note.title = form.student.data + ' Note '
        note.student_id = (User.query.filter_by(username=form.student.data).first()).id
        db.session.commit()
        flash('Your note has been updated!', 'success')
        return redirect(url_for('notes.notes_all', student="ALL"))
    elif request.method == 'GET':
        form.title.data = note.title
        form.student.data = (User.query.filter_by(id=note.student_id).first()).username

    return render_template('create_note.html', title='Update Note', form=form, legend = "Update Note")

@notes.route("/notes/<int:note_id>/delete", methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    date_now = datetime.datetime.now()
    activity = Activity(description=note.title+ " has been deleted!", student_id = note.student_id, 
                            author=current_user, date_posted = date_now)
    db.session.add(activity)
    delete_note = Note.__table__.delete().where(Note.id == note.id)
    db.session.execute(delete_note)
    db.session.commit()
    flash('Your note has been deleted!', 'success')
    return redirect(url_for('notes.notes_all', student="ALL"))
