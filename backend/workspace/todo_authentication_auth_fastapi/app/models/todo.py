from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base
from app.utils.auth import get_current_user
from app.models.user import User

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, title: str, description: str, owner_id: int):
        self.title = title
        self.description = description
        self.owner_id = owner_id

    def __repr__(self):
        return f"Todo(id={self.id}, title='{self.title}', description='{self.description}', completed={self.completed}, owner_id={self.owner_id}, created_at={self.created_at}, updated_at={self.updated_at})"

    @property
    def owner(self):
        return User.get_user_by_id(self.owner_id)

    @classmethod
    def get_todo_by_id(cls, todo_id: int):
        try:
            return cls.query.get(todo_id)
        except Exception as e:
            raise Exception(f"Failed to get todo by id: {e}")

    @classmethod
    def get_todos_by_owner_id(cls, owner_id: int):
        try:
            return cls.query.filter_by(owner_id=owner_id).all()
        except Exception as e:
            raise Exception(f"Failed to get todos by owner id: {e}")

    @classmethod
    def create_todo(cls, title: str, description: str):
        try:
            current_user = get_current_user()
            new_todo = cls(title, description, current_user.id)
            Base.session.add(new_todo)
            Base.session.commit()
            return new_todo
        except Exception as e:
            raise Exception(f"Failed to create todo: {e}")

    @classmethod
    def update_todo(cls, todo_id: int, title: str = None, description: str = None, completed: bool = None):
        try:
            todo = cls.get_todo_by_id(todo_id)
            if title:
                todo.title = title
            if description:
                todo.description = description
            if completed is not None:
                todo.completed = completed
            Base.session.commit()
            return todo
        except Exception as e:
            raise Exception(f"Failed to update todo: {e}")

    @classmethod
    def delete_todo(cls, todo_id: int):
        try:
            todo = cls.get_todo_by_id(todo_id)
            Base.session.delete(todo)
            Base.session.commit()
            return True
        except Exception as e:
            raise Exception(f"Failed to delete todo: {e}")