from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.models import Todo
from app.database import get_db
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.schemas import TodoSchema, TodoCreateSchema

router = APIRouter()

class TodoRequest(BaseModel):
    title: str
    description: str
    due_date: datetime

@router.get("/todos/")
async def read_todos(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    todos = db.query(Todo).filter(Todo.user_id == current_user["id"]).all()
    return todos

@router.post("/todos/")
async def create_todo(todo: TodoCreateSchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    new_todo = Todo(title=todo.title, description=todo.description, due_date=todo.due_date, user_id=current_user["id"])
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/todos/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id and Todo.user_id == current_user["id"]).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo

@router.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo: TodoCreateSchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    existing_todo = db.query(Todo).filter(Todo.id == todo_id and Todo.user_id == current_user["id"]).first()
    if existing_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    existing_todo.title = todo.title
    existing_todo.description = todo.description
    existing_todo.due_date = todo.due_date
    db.commit()
    db.refresh(existing_todo)
    return existing_todo

@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id and Todo.user_id == current_user["id"]).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}