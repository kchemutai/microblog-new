import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = '4fcb6ded09f29ed1452e6c53c059816a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['MAIL_SERVER']=os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT']=os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS']=os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')



mail=Mail(app)


db = SQLAlchemy(app)
bicrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from microblog import routes
