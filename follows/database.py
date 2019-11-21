# encoding: utf8
import datetime as dt
import enum
import json

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Follow(db.Model):
    __tablename__ = 'follow'
    user_id = db.Column(db.Integer, primary_key=True)
    followed_by_id= db.Column(db.Integer, primary_key=True)
    followed_by_name= db.Column(db.Unicode(128))

    def __init__(self, user, follower, follower_name, *args, **kw):
        self.user_id = user
        self.followed_by_id = follower
        self.followed_by_name = follower_name

"""
This function takes in input two user ids. Returns true if the second user
follows the first. 
"""
def isFollowing(who, by_who):
    return db.session.query(Follow).filter(Follow.followed_by_id == by_who).filter(Follow.user_id == who).count() > 0
