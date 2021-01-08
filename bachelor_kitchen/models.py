from bachelor_kitchen import app, db, login_manager
from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy.orm import relationship
import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    def get_id(self):
        return (self.username)

    username = db.Column(db.String(30), primary_key=True,
                         unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phonenum = db.Column(db.String(30), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    university = db.Column(db.String(255))
    address = db.Column(db.String(255))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zipcode = db.Column(db.String(10))
    profile = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    balance = db.Column(db.Float,nullable=True,default = 0)
    reservedposts = db.relationship(
        "ReservedPost", backref="author1", lazy=True)
    selfposts = db.relationship("Post", backref="author", lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.username}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    postid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    entries = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    cookingdate = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Time,nullable = False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    posteduser = db.Column(db.String(30), db.ForeignKey(
        'user.username'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class ReservedPost(db.Model):
    reserveid = db.Column(db.Integer, primary_key=True)
    originalpostid = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    entries = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    cookingdate = db.Column(db.DateTime, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    registereduser = db.Column(db.String(30), db.ForeignKey(
        'user.username'), nullable=False)

    def __repr__(self):
        return f"ReservedPost('{self.title}', '{self.date_posted}')"
