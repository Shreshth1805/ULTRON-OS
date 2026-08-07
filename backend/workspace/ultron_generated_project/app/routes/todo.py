from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from app.schemas.todo import TodoItem, TodoItemCreate, TodoItemUpdate
from app.services.todo_service import TodoService
from app.utils.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/todo", tags=["todo"])

class TodoRouter:
    def __init__(self, todo_service: TodoService):
        self.todo_service = todo_service

    def get_all(self, db: Session):
        return self.todo_service.get_all(db)

    def get_by_id(self, id: int, db: Session):
        return self.todo_service.get_by_id(id, db)

    def create(self, todo_item: TodoItemCreate, db: Session):
        return self.todo_service.create(todo_item, db)

    def update(self, id: int, todo_item: TodoItemUpdate, db: Session):
        return self.todo_service.update(id, todo_item, db)

    def delete(self, id: int, db: Session):
        return self.todo_service.delete(id, db)

todo_router = TodoRouter(TodoService())

@router.get("/", response_model=List[TodoItem])
def read_all(db: Session = Depends(get_db)):
    return todo_router.get_all(db)

@router.get("/{id}", response_model=TodoItem)
def read(id: int, db: Session = Depends(get_db)):
    db_todo = todo_router.get_by_id(id, db)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return db_todo

@router.post("/", response_model=TodoItem)
def create(todo_item: TodoItemCreate, db: Session = Depends(get_db)):
    return todo_router.create(todo_item, db)

@router.put("/{id}", response_model=TodoItem)
def update(id: int, todo_item: TodoItemUpdate, db: Session = Depends(get_db)):
    db_todo = todo_router.get_by_id(id, db)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return todo_router.update(id, todo_item, db)

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    db_todo = todo_router.get_by_id(id, db)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    todo_router.delete(id, db)
    return JSONResponse(status_code=200, content={"message": "Todo item deleted"})