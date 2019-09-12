from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
    )
from sqlalchemy.orm import relationship
from sqlalchemy.inspection import inspect
from sqlalchemy.sql.functions import func
from alayatodo.database import Base, db_session

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    # user = relationship(User, primaryjoin=user_id == User.id)
    description = Column(String(255))

    def __init__(self, user_id=None, description=None):
        self.user_id = user_id
        self.description = description

    def __repr__(self):
        return '<Todo %r>' % (self.description)

def get_todos_count():
    # db_session.query
    return db_session.query(func.count(Todo.id)).scalar()

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}