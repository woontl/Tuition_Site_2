from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404) #To handle 404 errors
def error_404(error):
    return render_template('errors/404.html'), 404 #returns second value which is the code

@errors.app_errorhandler(403) #To handle 403 errors
def error_403(error):
    return render_template('errors/403.html'), 403 #returns second value which is the code

@errors.app_errorhandler(500) #To handle 500 errors
def error_500(error):
    return render_template('errors/500.html'), 500 #returns second value which is the code

