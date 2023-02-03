from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Homework, Activity, Question, Working
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, UserDateForm, UserTopicsForm)
from flaskblog.users.utils import save_picture, send_reset_email
from datetime import datetime

users = Blueprint('users', __name__) #creating an instance, to be imported

@users.route("/register", methods=['GET', 'POST']) #Need to define methods here 
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, account_type=form.account_type.data, grade=form.grade.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success') #one time message flashed on screen
        return redirect(url_for('users.login')) #redirect to home if account created successfully
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() #DB query for email 
        if user and bcrypt.check_password_hash(user.password, form.password.data): #Check for email and password hash
            login_user(user, remember=form.remember.data) #Logins user + remember module
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home')) #redirect if next page exist, if not redirect to home
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/admin", methods=['GET', 'POST'])
@login_required #Requires login to view this route
def admin():
    if current_user.account_type == 'User':
        flash('You do not have access privileges to view this!', 'danger')
        return redirect(url_for('main.home'))
    users = User.query.all()
    return render_template('admin.html', title='Admin Panel', users=users)

@users.route("/admin/make_admin/<string:user_id>", methods=['GET', 'POST'])
@login_required #Requires login to view this route
def admin_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.account_type = "Admin"
    db.session.commit()
    flash(user.username +' has been made Admin!', 'success')
    return redirect(url_for('users.admin'))

@users.route("/admin/remove_admin/<string:user_id>", methods=['GET', 'POST'])
@login_required #Requires login to view this route
def remove_admin(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.account_type = "User"
    db.session.commit()
    flash('Admin access removed from ' + user.username + '!', 'success')
    return redirect(url_for('users.admin'))

@users.route("/admin/delete_user/<string:user_id>", methods=['GET', 'POST'])
@login_required #Requires login to view this route
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    name = user.username
    homework = Homework.query.filter_by(student_id=user_id).first()
    try:
        delete_working = Working.__table__.delete().where(Working.homework_id==homework.id)
        db.session.execute(delete_working)
    except:
        pass
    try:
        delete_qn = Question.__table__.delete().where(Question.homework_id==homework.id)
        db.session.execute(delete_qn)
    except:
        pass
    try:
        delete_activity = Activity.__table__.delete().where(Activity.student_id==user_id)
        db.session.execute(delete_activity)
    except:
        pass
    try:
        delete_hw = Homework.__table__.delete().where(Homework.student_id==user_id)
        db.session.execute(delete_hw)
    except:
        pass
    try:
        delete_user = User.__table__.delete().where(User.id == user_id)
        db.session.execute(delete_user)
    except:
        pass
    db.session.commit()
    flash(name + ' has been deleted!', 'success')
    return redirect(url_for('users.admin'))

@users.route("/account", methods=['GET', 'POST'])
@login_required #Requires login to view this route
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.grade = form.grade.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.grade.data = current_user.grade
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) #Define image_file variable with file path + jpg 
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route("/reset_password", methods=['GET', 'POST']) #To reset password
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit(): #if valid, send user an email with token
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user) #Triggers SMTP function
        flash('An email has been sent with instructions to reset your passsword.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You are now able to log in', 'success') #one time message flashed on screen
        return redirect(url_for('users.login')) #redirect to home if password updated successfully
    return render_template('reset_token.html', title='Reset Password', form=form)

@users.route("/user_dates/<string:username>", methods=['GET', 'POST'])
@login_required
def user_dates(username):
    form = UserDateForm()
    user = User.query.filter_by(username=username).first()
    if request.method == 'GET':
        pass
        form.description1.data = user.description1
        form.date1.data = user.date1
        form.time1.data = user.time1
        form.description2.data = user.description2
        form.date2.data = user.date2
        form.time2.data = user.time2
        form.description3.data = user.description3
        form.date3.data = user.date3
        form.time3.data = user.time3
        form.description4.data = user.description4
        form.date4.data = user.date4
        form.time4.data = user.time4
    elif request.method == 'POST':
        user.description1 = form.description1.data
        user.date1 = form.date1.data
        user.time1 = form.time1.data
        user.description2 = form.description2.data
        user.date2 = form.date2.data
        user.time2 = form.time2.data
        user.description3 = form.description3.data
        user.date3 = form.date3.data
        user.time3 = form.time3.data
        user.description4 = form.description4.data
        user.date4 = form.date4.data
        user.time4 = form.time4.data
        db.session.commit()
        flash(f'Your dates have been updated!', 'success')
        return redirect(url_for('main.home'))
    return render_template('user_dates.html', title='Dates', form=form)

@users.route("/user_topics/<string:username>", methods=['GET', 'POST'])
@login_required
def user_topics(username):
    form = UserTopicsForm()
    user = User.query.filter_by(username=username).first()
    if request.method == 'GET':
        if user.topics:
            topics_arr = user.topics.split(',')
            checks_arr = user.topics_check.split(',')
        else:
            topics_arr = []
            checks_arr = []
        
    elif request.method == 'POST':
        user.topics = ((request.form['action']).split(';'))[0]
        user.topics_check = ((request.form['action']).split(';'))[1]
        db.session.commit()
        flash(f'Your topics have been updated!', 'success')
        return redirect(url_for('main.home'))
    return render_template('user_topics.html', title='Dates', form=form, topics_arr=topics_arr, checks_arr=checks_arr)