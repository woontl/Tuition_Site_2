from dotenv import load_dotenv
import os #to setup env variables on personal com
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config, Anonymous
from flask_socketio import SocketIO

db = SQLAlchemy() #Create DB instance
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' #Requires login to view
login_manager.login_message_category = 'info'
login_manager.anonymous_user = Anonymous
mail = Mail()
socketio = SocketIO()


def create_app(config_class=Config):
    app = Flask(__name__) #Setting an instance of this flask class. __name__ will be set as __main__when ran. But __name__ will be set as another name if importing another module
    app.config.from_object(Config)

    socketio.init_app(app, cors_allowed_origins="*")
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.main.routes import main
    from flaskblog.notes.routes import notes
    from flaskblog.resources.routes import resources
    from flaskblog.homeworks.routes import homeworks
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(notes)
    app.register_blueprint(resources)
    app.register_blueprint(homeworks)
    app.register_blueprint(errors)

    return app
