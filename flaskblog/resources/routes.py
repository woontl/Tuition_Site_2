from flask import render_template as real_render_template, Blueprint
from flask_login import login_required, current_user
from flaskblog.models import Changelog, Activity
import datetime as datetime

resources = Blueprint('resources', __name__) #creating an instance, to be imported

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


@resources.route("/IB_resources")
@login_required
def IB_resources():
    return render_template('IB_resources.html', title='IB_Resources')

@resources.route("/IGCSE_resources")
@login_required
def IGCSE_resources():
    return render_template('IGCSE_resources.html', title='IGCSE_Resources')

@resources.route("/IB_topical_questions")
@login_required
def IB_topical_questions():
    return render_template('IB_topical_questions.html', title='IB_topical_questions')

@resources.route("/IB_key_concepts")
@login_required
def IB_key_concepts():
    return render_template('IB_key_concepts.html', title='IB_key_concepts')

@resources.route("/IB_tutorial_videos")
@login_required
def IB_tutorial_videos():
    return render_template('IB_tutorial_videos.html', title='IB_tutorial_videos')

@resources.route("/IB_practice_papers")
@login_required
def IB_practice_papers():
    return render_template('IB_practice_papers.html', title='IB_practice_papers')

@resources.route("/IGCSE_topical_questions")
@login_required
def IGCSE_topical_questions():
    return render_template('IGCSE_topical_questions.html', title='IGCSE_topical_questions')

@resources.route("/IGCSE_key_concepts")
@login_required
def IGCSE_key_concepts():
    return render_template('IGCSE_key_concepts.html', title='IGCSE_key_concepts')

@resources.route("/IGCSE_tutorial_videos")
@login_required
def IGCSE_tutorial_videos():
    return render_template('IGCSE_tutorial_videos.html', title='IGCSE_tutorial_videos')

@resources.route("/IGCSE_practice_papers")
@login_required
def IGCSE_practice_papers():
    return render_template('IGCSE_practice_papers.html', title='IGCSE_practice_papers')