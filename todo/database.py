from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todo.models import Base

DATABASE_URL = "postgresql://postgres:postgres@localhost/todo_db"

engine = create_engine(DATABASE_URL,echo = True) #When you set echo=True, SQLAlchemy will print all the SQL statements it sends to the database to the console or standard output. 

'''
SessionMaker = sessionmaker(
    autocommit = False #after adding objects to the session (like with db.add()), you need to explicitly call db.commit() to save changes to the database.
    autoflush=False # would need to explicitly call db.flush() if you want to push data to the database before a query.
    bind = engine
)
'''

SessionMaker = sessionmaker(
    autocommit = False,autoflush=False ,bind = engine
)


def init_db():
    Base.metadata.create_all(bind=engine)