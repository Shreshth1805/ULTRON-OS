from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.utils.config import get_config
from app.models.todo import Todo

Base = declarative_base()

class Database:
    def __init__(self):
        self.config = get_config()
        self.engine = create_engine(self.config['DATABASE_URL'])
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

    def close_session(self, session):
        session.close()

    def get_all_todos(self, session):
        return session.query(Todo).all()

    def get_todo(self, session, id):
        return session.query(Todo).filter(Todo.id == id).first()

    def create_todo(self, session, title, description):
        todo = Todo(title=title, description=description, completed=False, created_at=func.now())
        session.add(todo)
        session.commit()
        return todo

    def update_todo(self, session, id, title, description, completed):
        todo = session.query(Todo).filter(Todo.id == id).first()
        if todo:
            todo.title = title
            todo.description = description
            todo.completed = completed
            session.commit()
            return todo
        return None

    def delete_todo(self, session, id):
        todo = session.query(Todo).filter(Todo.id == id).first()
        if todo:
            session.delete(todo)
            session.commit()
            return True
        return False

database = Database()