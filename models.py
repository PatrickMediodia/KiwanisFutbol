from app import db , login_manager , app
from flask_login import UserMixin , LoginManager
from datetime import datetime

class Registered(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100),nullable =False)
    ageGroup = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)   
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return str(self.id)

class Admin(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),nullable =False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


