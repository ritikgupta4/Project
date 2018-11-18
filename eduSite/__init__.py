from flask import Flask                 #import Flask class
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager 

app = Flask(__name__)                   #create an instance of class Flask
app.config['SECRET_KEY'] = '00e6a25084c0fd1c76362b6a516bbc28'    #https://docs.python.org/3/library/secrets.html
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from eduSite import routes