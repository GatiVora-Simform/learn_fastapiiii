from pydantic import BaseModel
from datetime import datetime

class TodoBase(BaseModel):
    task:str
    is_done:bool

class Todo(TodoBase):
    id:int
    created_at:datetime

    class Config:
        orm_mode=True #orm_mode = True is like telling FastAPI: “Hey, the data you get isn’t a dictionary — it’s a Python object. Look at its .id, .task, .is_done values.”
    
class UserBase(BaseModel):
    username:str

class UserCreate(UserBase):
    password:str

class UserOut(UserBase):
    id:int
    class Config:
        orm_mode=True