from flask import render_template, Blueprint
from flask_login import login_required

resources = Blueprint('resources', __name__) #creating an instance, to be imported

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