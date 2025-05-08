from fastapi import FastAPI, Depends, HTTPException
from todo.auth import ALGORITHM, SECRET_KEY, create_token, hash_password, verify_password
from todo.crud import create_todo, delete_todo, get_all_todos, get_todo, update_todo
from todo.database import SessionMaker,engine
from todo.models import Base, User
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from todo.schemas import Todo, TodoBase, UserCreate

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
    

@app.post('/register')
def register_user(user:UserCreate,db:Session = Depends(get_db)):
    hashed = hash_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username}
