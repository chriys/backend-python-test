from flask import Flask
import sqlite3
from alayatodo.database import db_session

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


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


import alayatodo.views