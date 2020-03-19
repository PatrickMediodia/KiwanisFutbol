from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , UserMixin , login_user , login_required , logout_user
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registered.db'
app.secret_key = os.urandom(24)
app.debug = True

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)

from views import * 
from models import *

if __name__ == "__main__":
    app.run(debug=True) 