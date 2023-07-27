from sqlalchemy.sql import func 
from . import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    notes = db.relationship('Notes', backref='users', lazy=True)

class Notes(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(255))
    date = db.Column(db.DateTime(timezone = True), default= func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
     