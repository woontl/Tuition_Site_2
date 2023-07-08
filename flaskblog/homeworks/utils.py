import os
from pickletools import optimize
import secrets
from PIL import Image
from flask import current_app, url_for
import re
from flaskblog import mail
import base64

def save_qn_picture(form_picture):
    random_hex = secrets.token_hex(8) #Renaming user input filename with hex
    _, f_ext = os.path.splitext(form_picture.filename) #Split file name up
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/questionbank',picture_fn)
    
    #output_size = (125,125) #resizing image
    i = Image.open(form_picture)
    i.save(picture_path, optimize=True, quality=50) #saving hexed file name in directory

    return picture_fn

def save_working_picture(form_picture):
    random_hex = secrets.token_hex(8) #Renaming user input filename with hex
    image_data = form_picture.split(",")[1]
    image_bytes = base64.b64decode(image_data)
    picture_fn = 'screenshot_' + random_hex + '.png'
    picture_path = os.path.join(current_app.root_path,'static/questionbank', picture_fn)

    with open(picture_path, "wb") as file:
        file.write(image_bytes)

    return picture_fn

def MQ_formatter(MQ):
    MQ = re.sub('\(','',MQ)
    MQ = re.sub('\)','',MQ)
    MQ = re.sub('【','',MQ)
    MQ = re.sub('】','',MQ)
    MQ = re.sub('\'','',MQ)
    MQ = re.sub('\{','',MQ)
    MQ = re.sub('\}','',MQ)
    return MQ