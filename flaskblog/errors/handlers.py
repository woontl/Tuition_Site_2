from flask import Blueprint, render_template as real_render_template
from flaskblog.models import Changelog, Activity
from flask_login import current_user, login_required
import datetime as datetime

errors = Blueprint('errors', __name__)

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


@errors.app_errorhandler(404) #To handle 404 errors
def error_404(error):
    return render_template('errors/404.html'), 404 #returns second value which is the code

@errors.app_errorhandler(403) #To handle 403 errors
def error_403(error):
    return render_template('errors/403.html'), 403 #returns second value which is the code

@errors.app_errorhandler(500) #To handle 500 errors
def error_500(error):
    return render_template('errors/500.html'), 500 #returns second value which is the code

