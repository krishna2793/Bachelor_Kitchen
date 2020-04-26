from bachelor_kitchen import app, db, login_manager
from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


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
    photo = db.Column(db.String(20), nullable=True)
    selfposts = db.relationship("Post", backref="author", lazy=True)
    #acceptedposts=relationship("Post", backref="acceptedusers", lazy=True)
    # otp = db.Column(db.String(6))
    # status = db.Column(db.String(20), nullable=False)
    # loginattempts = db.Column(db.Integer, default=0)
    # loginactive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(db.Model):
    postid = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    entries = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    cookingdate = db.Column(db.DateTime, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    posteduser = db.Column(db.String(30), db.ForeignKey(
        'user.username'), nullable=False)
    #acceptedusers=db.Column(db.String(30),db.ForeignKey('user.username'), nullable=False)
