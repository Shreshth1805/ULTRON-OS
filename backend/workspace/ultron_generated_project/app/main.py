from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from app.utils.config import settings
from app.utils.database import SessionLocal, engine
from app.models import todo
from app.schemas import todo as schemas
from app.services import todo_service
from sqlalchemy.orm import Session

app = FastAPI(
    title="Todo API",
    description="A simple Todo API",
    version="1.0.0",
    contact={
        "name": "ULTRON",
        "email": "ultron@example.com",
    },
)

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/todos/")
def read_todos(db: Session = Depends(get_db)):
    todos = todo_service.get_all_todos(db)
    return todos

@app.get("/todos/{todo_id}")
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = todo_service.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos/")
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return todo_service.create_todo(db, todo)

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo_service.update_todo(db, todo_id, todo)
    return {"message": "Todo updated successfully"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_service.delete_todo(db, todo_id)
    return {"message": "Todo deleted successfully"}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}