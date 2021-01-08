from bachelor_kitchen import models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import logging
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.environ.get('SECRET_KEY', ''))
app.config['SQLALCHEMY_DATABASE_URI'] = str(os.environ.get('SQLALCHEMY_DATABASE_URI', ''))
logger = logging.getLogger()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


db.drop_all()
db.create_all()
from bachelor_kitchen import routes
