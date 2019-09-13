from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean
    )
from sqlalchemy.orm import relationship
from sqlalchemy.inspection import inspect
from sqlalchemy.sql.functions import func
from alayatodo.database import Base, db_session
from alayatodo import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class User(Base):
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

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, primaryjoin=user_id == User.id)
    description = Column(String(255))
    completed = Column(Boolean(create_constraint=True))

    def __init__(self, user_id=None, description=None, completed=False):
        self.user_id = user_id
        self.description = description
        self.completed = completed

    def __repr__(self):
        return '<Todo %r>' % (self.description)

def get_todos_count(user_id):
    return db_session.query(func.count(Todo.id)).filter(Todo.user_id == user_id).scalar()

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}