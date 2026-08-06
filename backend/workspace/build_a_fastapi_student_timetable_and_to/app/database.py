from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel

SQLALCHEMY_DATABASE_URL = "sqlite:///student.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Timetable(Base):
    __tablename__ = "timetables"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    subject = Column(String)
    time = Column(DateTime)
    day = Column(String)

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    task = Column(String)
    deadline = Column(DateTime)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

class StudentModel(BaseModel):
    username: str
    email: str
    password: str

class TimetableModel(BaseModel):
    student_id: int
    subject: str
    time: datetime
    day: str

class TodoModel(BaseModel):
    student_id: int
    task: str
    deadline: datetime
    completed: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()