from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app= Flask(__name__)
app.config['SECRET_KEY']= '5a0705d29e5038ebe7a8ae2b088c7a62'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category= 'info'
db = SQLAlchemy(app)

from appmain import routes