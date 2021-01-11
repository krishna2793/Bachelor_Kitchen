
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import logging
import datetime
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.environ.get('SECRET_KEY', ''))
app.config['SQLALCHEMY_DATABASE_URI'] = str(os.environ.get('DATABASE_URL', ''))
logger = logging.getLogger()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}
app.config.update(mail_settings)
mail = Mail(app)

from bachelor_kitchen import models

#db.drop_all()
#db.create_all()

from bachelor_kitchen import routes
