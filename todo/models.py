import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy import func

Base = declarative_base()

class Todo(Base):
    """A simple todo list model."""

    __tablename__ = 'todos'

    id = Column(Integer,primary_key = True)
    task = Column(String)
    is_done= Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())


class User(Base):
    """A simple user model."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String,unique = True)
    hashed_password = Column(String)