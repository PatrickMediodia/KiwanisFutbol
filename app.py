from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , UserMixin , login_user , login_required , logout_user
from flask_mail import Mail , Message

app = Flask(__name__)

if app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig')
elif app.config['ENV'] == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
login_manager = LoginManager()
mail = Mail(app)

db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

from views import * 
from models import *

if __name__ == "__main__":
    app.run(debug=True) 