from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TodoResponse(BaseModel):
    todo: Todo

    class Config:
        orm_mode = True

class TodoListResponse(BaseModel):
    todos: list[Todo]

    class Config:
        orm_mode = True