from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<User {}>'.format(self.username) 
    # def __tablename__(self):
    #     return "users"
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class StorageList(db.Model):
    __tablename__ = "storage"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    box_num = db.Column(db.Integer)
    content = db.Column(db.String(200),index=True)
    def __init__(self, box_num, content):
        self.box_num = box_num
        self.content = content

class Boxes(db.Model):
    __tablename__ = "layout"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    z = db.Column(db.Integer)
    box_num = db.Column(db.Integer)


class Job:
    def __init__(self, job_id, box_num, status = "inactive"):
        self.job_id = job_id
        self.box_num = box_num
        self.status = status