from typing import Dict, List
from sqlalchemy.orm import Session
from app.models import Todo, User
from app.schemas import TodoCreate, TodoUpdate, UserCreate, UserUpdate
from app.utils.auth import get_password_hash, verify_password
from app.config import settings

class TodoService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_todos(self) -> List[Todo]:
        return self.db.query(Todo).all()

    def get_todo(self, todo_id: int) -> Todo:
        return self.db.query(Todo).filter(Todo.id == todo_id).first()

    def create_todo(self, todo: TodoCreate) -> Todo:
        db_todo = Todo(**todo.dict())
        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo

    def update_todo(self, todo_id: int, todo: TodoUpdate) -> Todo:
        db_todo = self.get_todo(todo_id)
        if not db_todo:
            raise ValueError("Todo not found")
        for key, value in todo.dict(exclude_unset=True).items():
            setattr(db_todo, key, value)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo

    def delete_todo(self, todo_id: int) -> None:
        db_todo = self.get_todo(todo_id)
        if not db_todo:
            raise ValueError("Todo not found")
        self.db.delete(db_todo)
        self.db.commit()

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()

    def get_user(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        db_user = User(**user.dict(exclude={"password"}), hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user: UserUpdate) -> User:
        db_user = self.get_user(user_id)
        if not db_user:
            raise ValueError("User not found")
        for key, value in user.dict(exclude_unset=True).items():
            if key == "password":
                db_user.hashed_password = get_password_hash(value)
            else:
                setattr(db_user, key, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> None:
        db_user = self.get_user(user_id)
        if not db_user:
            raise ValueError("User not found")
        self.db.delete(db_user)
        self.db.commit()

    def authenticate_user(self, username: str, password: str) -> User:
        db_user = self.get_user_by_username(username)
        if not db_user:
            raise ValueError("User not found")
        if not verify_password(password, db_user.hashed_password):
            raise ValueError("Invalid password")
        return db_user

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

services = {
    "todo": TodoService,
    "user": UserService
}