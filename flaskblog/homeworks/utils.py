import os
from pickletools import optimize
import secrets
from PIL import Image
from flask import current_app
import re

def save_qn_picture(form_picture):
    random_hex = secrets.token_hex(8) #Renaming user input filename with hex
    _, f_ext = os.path.splitext(form_picture.filename) #Split file name up
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/questionbank',picture_fn)
    
    #output_size = (125,125) #resizing image
    i = Image.open(form_picture)
    i.save(picture_path, optimize=True, quality=50) #saving hexed file name in directory

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