```python
import pytest
from database import Base, engine, SessionLocal, Student, Timetable, Todo, StudentModel, TimetableModel, TodoModel, get_db
from sqlalchemy.orm import sessionmaker
from datetime import datetime

@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_student(db):
    student = Student(username="test", email="test@example.com", password="password")
    db.add(student)
    db.commit()
    assert db.query(Student).first().username == "test"

def test_create_timetable(db):
    student = Student(username="test", email="test@example.com", password="password")
    db.add(student)
    db.commit()
    timetable = Timetable(student_id=1, subject="Math", time=datetime.now(), day="Monday")
    db.add(timetable)
    db.commit()
    assert db.query(Timetable).first().subject == "Math"

def test_create_todo(db):
    student = Student(username="test", email="test@example.com", password="password")
    db.add(student)
    db.commit()
    todo = Todo(student_id=1, task="Homework", deadline=datetime.now(), completed=False)
    db.add(todo)
    db.commit()
    assert db.query(Todo).first().task == "Homework"

def test_student_model():
    student = StudentModel(username="test", email="test@example.com", password="password")
    assert student.username == "test"

def test_timetable_model():
    timetable = TimetableModel(student_id=1, subject="Math", time=datetime.now(), day="Monday")
    assert timetable.subject == "Math"

def test_todo_model():
    todo = TodoModel(student_id=1, task="Homework", deadline=datetime.now(), completed=False)
    assert todo.task == "Homework"

def test_get_db():
    db = get_db()
    assert db is not None

def test_create_all_tables():
    Base.metadata.create_all(bind=engine)
    assert engine.has_table("students")
    assert engine.has_table("timetables")
    assert engine.has_table("todos")

def test_session_local():
    db = SessionLocal()
    assert db is not None

def test_base():
    assert Base is not None

def test_engine():
    assert engine is not None

def test_sessionmaker():
    assert SessionLocal is not None
```