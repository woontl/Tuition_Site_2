import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #Renaming user input filename with hex
    _, f_ext = os.path.splitext(form_picture.filename) #Split file name up
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pics',picture_fn)
    
    output_size = (125,125) #resizing image
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) #saving hexed file name in directory

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
    
def send_HW_alert(user):
    msg = Message('New Homework Assignment',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''Hi '''+str(user.username)+'''! A new homework assignment has been posted. Visit the following link: '''+\
    str(url_for('main.home', _external=True))
    mail.send(msg)

def send_account_approval(user):
    msg = Message('Account Approval',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''Hi '''+str(user.username)+'''! Your account has been approved. Kindly login using the following link: '''+\
    str(url_for('main.home', _external=True))
    mail.send(msg)

def send_enquiry_confirmation(name, email):
    msg = Message('Enquiry Received',
                  sender='noreply@demo.com',
                  recipients=[email])
    msg.body = f'''Hi '''+str(name)+'''! Your enquiry has been received. Our team will reach out to you in 1-3 business days '''
    mail.send(msg)

def send_enquiry_self(name, age, number, email, school, grade, syllabus, content):
    msg = Message('New Enquiry',
                  sender='noreply@demo.com',
                  recipients=['donotreply.mathinthesky@gmail.com'])
    # Create the email body in the desired format
    msg.body = f'''Hi boss! Please see the new enquiry below:

    Name: {name}
    Age: {age}
    Number: {number}
    Email: {email}
    School: {school}
    Grade: {grade}
    Syllabus: {syllabus}

    Enquiry Content:
    {content}
    '''
    mail.send(msg)