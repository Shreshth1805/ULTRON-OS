from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.models import Student, Timetable, Todo
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

class StudentBase(BaseModel):
    name: str
    email: str

class StudentCreate(StudentBase):
    password: str

class Student(StudentBase):
    id: int
    timetable: List[Timetable]
    todo: List[Todo]

    class Config:
        orm_mode = True

class TimetableBase(BaseModel):
    day: str
    time: str
    subject: str

class TimetableCreate(TimetableBase):
    pass

class Timetable(TimetableBase):
    id: int
    student_id: int

    class Config:
        orm_mode = True

class TodoBase(BaseModel):
    title: str
    description: str
    due_date: datetime

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    student_id: int

    class Config:
        orm_mode = True

pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_student(db: Session, email: str, password: str):
    student = db.query(Student).filter(Student.email == email).first()
    if not student:
        return False
    if not verify_password(password, student.password):
        return False
    return student

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secretkey", algorithm="HS256")
    return encoded_jwt

@router.post("/login", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    student = authenticate_student(get_db(), form_data.username, form_data.password)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": student.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/students/me", response_model=Student)
async def read_students_me(token: str = Depends(oauth2_scheme)):
    db = get_db()
    student = db.query(Student).filter(Student.email == token).first()
    return student

@router.post("/students/", response_model=Student)
async def create_student(student: StudentCreate):
    db = get_db()
    hashed_password = get_password_hash(student.password)
    db_student = Student(name=student.name, email=student.email, password=hashed_password)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/students/", response_model=List[Student])
async def read_students():
    db = get_db()
    students = db.query(Student).all()
    return students

@router.get("/students/{student_id}", response_model=Student)
async def read_student(student_id: int):
    db = get_db()
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/students/{student_id}/timetable", response_model=Timetable)
async def create_timetable(student_id: int, timetable: TimetableCreate):
    db = get_db()
    db_timetable = Timetable(day=timetable.day, time=timetable.time, subject=timetable.subject, student_id=student_id)
    db.add(db_timetable)
    db.commit()
    db.refresh(db_timetable)
    return db_timetable

@router.get("/students/{student_id}/timetable", response_model=List[Timetable])
async def read_timetable(student_id: int):
    db = get_db()
    timetable = db.query(Timetable).filter(Timetable.student_id == student_id).all()
    return timetable

@router.post("/students/{student_id}/todo", response_model=Todo)
async def create_todo(student_id: int, todo: TodoCreate):
    db = get_db()
    db_todo = Todo(title=todo.title, description=todo.description, due_date=todo.due_date, student_id=student_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/students/{student_id}/todo", response_model=List[Todo])
async def read_todo(student_id: int):
    db = get_db()
    todo = db.query(Todo).filter(Todo.student_id == student_id).all()
    return todo