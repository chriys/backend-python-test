from flask import Flask
import sqlite3
from alayatodo.database import db_session
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import pretty, datetime

# configuration
DATABASE = '/tmp/alayatodo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % app.config['DATABASE']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login = LoginManager(app)
login.login_view = 'login'

csrf = CSRFProtect()
csrf.init_app(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.context_processor
def utility_processor():

    def timeago(date):
        return pretty.date(date)

    return dict(timeago=timeago)

import alayatodo.views
