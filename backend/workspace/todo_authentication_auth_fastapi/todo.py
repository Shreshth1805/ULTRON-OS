from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base
from app.utils.auth import get_current_user
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime
from typing import List

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class TodoSchema(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TodoCreate(BaseModel):
    title: str
    description: str

class TodoUpdate(BaseModel):
    title: str | None
    description: str | None
    completed: bool | None

class TodoService:
    def get_all_todos(self, current_user: int):
        return Todo.query.filter_by(owner_id=current_user).all()

    def get_todo(self, todo_id: int, current_user: int):
        return Todo.query.filter_by(id=todo_id, owner_id=current_user).first()

    def create_todo(self, todo: TodoCreate, current_user: int):
        new_todo = Todo(title=todo.title, description=todo.description, owner_id=current_user)
        Base.metadata.bind.engine.execute(Todo.__table__.insert().values(new_todo.__dict__))
        return new_todo

    def update_todo(self, todo_id: int, todo: TodoUpdate, current_user: int):
        existing_todo = Todo.query.filter_by(id=todo_id, owner_id=current_user).first()
        if existing_todo:
            if todo.title:
                existing_todo.title = todo.title
            if todo.description:
                existing_todo.description = todo.description
            if todo.completed is not None:
                existing_todo.completed = todo.completed
            Base.metadata.bind.engine.execute(Todo.__table__.update().where(Todo.id == todo_id).values(existing_todo.__dict__))
            return existing_todo
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    def delete_todo(self, todo_id: int, current_user: int):
        todo = Todo.query.filter_by(id=todo_id, owner_id=current_user).first()
        if todo:
            Base.metadata.bind.engine.execute(Todo.__table__.delete().where(Todo.id == todo_id))
            return {"message": "Todo deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

class TodoRouter:
    def __init__(self, todo_service: TodoService):
        self.todo_service = todo_service

    def get_all_todos(self, current_user: int = Depends(get_current_user)):
        return self.todo_service.get_all_todos(current_user)

    def get_todo(self, todo_id: int, current_user: int = Depends(get_current_user)):
        return self.todo_service.get_todo(todo_id, current_user)

    def create_todo(self, todo: TodoCreate, current_user: int = Depends(get_current_user)):
        return self.todo_service.create_todo(todo, current_user)

    def update_todo(self, todo_id: int, todo: TodoUpdate, current_user: int = Depends(get_current_user)):
        return self.todo_service.update_todo(todo_id, todo, current_user)

    def delete_todo(self, todo_id: int, current_user: int = Depends(get_current_user)):
        return self.todo_service.delete_todo(todo_id, current_user)