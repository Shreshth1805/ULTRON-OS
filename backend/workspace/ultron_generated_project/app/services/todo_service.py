from app.models.todo import Todo
from app.utils.database import SessionLocal
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session

class TodoService:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_todos(self) -> List[Todo]:
        return self.db.query(Todo).all()

    def get_todo(self, todo_id: int) -> Todo:
        return self.db.query(Todo).filter(Todo.id == todo_id).first()

    def create_todo(self, title: str, description: str) -> Todo:
        new_todo = Todo(title=title, description=description)
        self.db.add(new_todo)
        self.db.commit()
        self.db.refresh(new_todo)
        return new_todo

    def update_todo(self, todo_id: int, title: str, description: str) -> Todo:
        todo = self.get_todo(todo_id)
        if todo:
            todo.title = title
            todo.description = description
            self.db.commit()
            self.db.refresh(todo)
        return todo

    def delete_todo(self, todo_id: int) -> bool:
        todo = self.get_todo(todo_id)
        if todo:
            self.db.delete(todo)
            self.db.commit()
            return True
        return False

    def close_session(self):
        self.db.close()