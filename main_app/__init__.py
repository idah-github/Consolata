import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///" + os.path.join(basedir,"storage.db")
app.config['SQLALCHEMY_TRACK_MODIFICATION']= False
app.config['POST_UPLOAD_FOLDER']  = os.path.join(basedir,'static/images/post/')
app.config['IMAGE_UPLOAD_FOLDER'] = os.path.join(basedir, 'static/images/profiles/')
db= SQLAlchemy(app)
login_manager= LoginManager()

login_manager.init_app(app)
login_manager.login_view ="login"