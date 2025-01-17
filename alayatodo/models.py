from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
    )
from sqlalchemy.orm import relationship
from sqlalchemy.inspection import inspect
from sqlalchemy.sql.functions import func
from alayatodo.database import Base, db_session
from alayatodo import app, login
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime
from datetime import datetime
from dateutil import tz

bcrypt = Bcrypt(app)

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    todos = relationship('Todo')

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id).encode("utf-8").decode("utf-8")

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, primaryjoin=user_id == User.id)
    description = Column(String(255))
    completed_at = Column(DateTime())
    updated_at = Column(DateTime())
    _created_at = Column('created_at', DateTime())

    def __init__(self, user_id=None, description=None, completed_at=None, updated_at=None, created_at=None):
        self.user_id = user_id
        self.description = description
        self.completed_at = completed_at
        self.updated_at = updated_at
        self._created_at = created_at

    def __repr__(self):
        return '<Todo %r>' % (self.description)

    @property
    def completed(self):
        return self.completed_at != None

    @property
    def created_at(self):
        # add timezone info
        utc = self._created_at.replace(tzinfo=tz.tzutc())
        # Convert to local timezone and remove timezone info
        return utc.astimezone(tz.tzlocal()).replace(tzinfo=None)

    @created_at.setter
    def created_at(self, created_at):
        self._created_at = created_at

    def toggle_completion(self):
        if not self.completed:
            self.completed_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            self.completed_at = None
            self.updated_at = datetime.now()

    def belongs_to(self, user_id):
        return self.user_id == user_id

def get_todos_count(user_id):
    return db_session.query(func.count(Todo.id)).filter(Todo.user_id == user_id).scalar()

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
