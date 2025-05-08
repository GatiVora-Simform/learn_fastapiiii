from fastapi import HTTPException
from sqlalchemy.orm import Session

from todo.models import Todo
from todo.schemas import TodoBase

def get_all_todos(db:Session):
    return db.query(Todo).all()

def get_todo( id:int,db:Session):
    todo= db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

def create_todo(todo:TodoBase,db:Session):
    db_todo = Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(id:int,todo:TodoBase,db:Session):
    db_todo = get_todo(id,db)
    db_todo.task = todo.task
    db_todo.is_done = todo.is_done
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(id:int,db:Session):
    db_todo = get_todo(id,db)
    db.delete(db_todo)
    db.commit()
    return {"message":"Todo deleted"}  # return a message instead of the todo object


