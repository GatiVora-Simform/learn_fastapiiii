from fastapi import FastAPI, Depends, HTTPException
from todo.crud import create_todo, delete_todo, get_all_todos, get_todo, update_todo
from todo.database import SessionMaker,engine
from todo.models import Base
from sqlalchemy.orm import Session

from todo.schemas import Todo, TodoBase
app = FastAPI()

def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

@app.get('/todos')
def read_todos(db:Session = Depends(get_db)):
    return get_all_todos(db)

@app.post('/todos')
def add_todos(todo:TodoBase,db:Session = Depends(get_db)):
    return create_todo(todo,db)

@app.get('/todos/{todo_id}')
def read_todo(todo_id:int,db:Session = Depends(get_db)):
    return get_todo(todo_id,db)

# @app.put('todos/{todo_id}')
# def updatee_todo(todo_id:int,todo:TodoBase,db:Session = Depends(get_db)):
#     return update_todo(todo_id,todo,db)

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo_item(todo_id: int, todo: TodoBase, db: Session = Depends(get_db)):
    try:
        return update_todo( todo_id, todo,db)
    except :
        raise HTTPException(status_code=404, detail="Todo not found")
    
@app.delete('/todos/{todo_id}')
def delete_todo_item(todo_id:int,db:Session=Depends(get_db)):
    try:
        return delete_todo(todo_id,db)
    except :
        raise HTTPException(status_code=404, detail="Todo not found")