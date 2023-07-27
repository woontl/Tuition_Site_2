from flask import render_template as real_render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Homework, Activity, Question, Working, Changelog
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, ContactForm)
from flaskblog.users.utils import save_picture, send_reset_email, send_HW_alert, send_account_approval, send_enquiry_confirmation, send_enquiry_self
import datetime as datetime
from sqlalchemy import text

users = Blueprint('users', __name__) #creating an instance, to be imported

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

@users.route("/signup", methods=['GET', 'POST']) #Need to define methods here 
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, 
                    account_type='User', grade=(form.grade.data)[6:], verified = 0, dark_mode = 'on')
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created and is pending approval. An email will be sent out once approved!', 'success') #one time message flashed on screen
        return redirect(url_for('main.landing_page')) #redirect to home if account created successfully
    return render_template('signup.html', title='Sign Up', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        email_or_username = form.email.data

        # Check if input is a valid email address
        if '@' in email_or_username:
            user = User.query.filter_by(email=email_or_username).first()
        else:
            user = User.query.filter_by(username=email_or_username).first()

        if user.verified == 0:
            flash('Login unsuccessful. Account is still pending approval!', 'danger')
        
        elif user and bcrypt.check_password_hash(user.password, form.password.data): #Check for email and password hash
            login_user(user, remember=form.remember.data) #Logins user + remember module
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home')) #redirect if next page exist, if not redirect to home
        else:
            flash('Login unsuccessful. Please check email and password!', 'danger')
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
    hw_list = Homework.query.filter_by(student_id=user_id).all()
    hw_id_list = [homework.id for homework in hw_list]
    try:
        delete_working = Working.__table__.delete().where(Working.homework_id.in_(hw_id_list))
        db.session.execute(delete_working)
    except:
        pass
    try:
        delete_qn = Question.__table__.delete().where(Question.homework_id.in_(hw_id_list))
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

@users.route("/settings/<string:username>", methods=['GET', 'POST'])
@login_required #Requires login to view this route
def settings(username):
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if username == 'ALL':
            user = current_user
        else:
            user = User.query.filter_by(username = username).first()
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        user.dark_mode = request.form.get('dark_mode')

        # Use the text() function to create a SQL expression with the REPLACE function
        old_name = user.username
        new_name = form.username.data
        update_query = text("UPDATE activity SET description = REPLACE(description, :old_name, :new_name)")
        db.session.execute(update_query, {"old_name": old_name, "new_name": new_name})
        update_query = text("UPDATE lesson SET title = REPLACE(title, :old_name, :new_name)")
        db.session.execute(update_query, {"old_name": old_name, "new_name": new_name})
        update_query = text("UPDATE homework SET title = REPLACE(title, :old_name, :new_name)")
        db.session.execute(update_query, {"old_name": old_name, "new_name": new_name})

        user.username = form.username.data
        user.email = form.email.data
        user.grade = form.grade.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.settings', username = username))
    elif request.method == 'GET':
        if username == 'ALL':
            user = current_user
        else:
            user = User.query.filter_by(username = username).first()
        form.username.data = user.username
        form.email.data = user.email
        form.grade.data = user.grade
    image_file = url_for('static', filename='profile_pics/' + user.image_file) #Define image_file variable with file path + jpg 
    return render_template('settings.html', image_file=image_file, form=form, user=user)

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

@users.route("/HW_alert/<string:username>", methods=['GET', 'POST'])
@login_required
def HW_alert(username):
    user = User.query.filter_by(username=username).first()
    send_HW_alert(user)
    flash(f'HW alert has been sent to ' + user.username +'!', 'success')
    return redirect(url_for('users.admin'))

@users.route("/verify/<string:username>", methods=['GET', 'POST'])
@login_required
def verify(username):
    user = User.query.filter_by(username=username).first()
    user.verified = 1
    db.session.commit()
    send_account_approval(user)
    flash(f'Account approval email has been sent to ' + user.username +'!', 'success')
    return redirect(url_for('users.admin'))

@users.route("/contact", methods=['GET', 'POST']) #Need to define methods here 
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        number = form.number.data
        email = form.email.data
        school = form.school.data
        grade = form.grade.data
        syllabus = form.syllabus.data
        content = form.enquiry.data
        send_enquiry_confirmation(name, email)
        send_enquiry_self(name, age, number, email, school, grade, syllabus, content)
        db.session.commit()
        flash(f'Your enquiry has been received! Our team will reach out to you in 1-3 business days!', 'success') #one time message flashed on screen
        return redirect(url_for('users.contact'))
    return render_template('contact.html', title='Contact Us', form=form)