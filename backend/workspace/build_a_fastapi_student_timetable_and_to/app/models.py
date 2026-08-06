from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class StudentBase(BaseModel):
    student_id: str
    name: str
    email: str

class Student(StudentBase):
    id: int
    password: str
    class Config:
        orm_mode = True

class StudentCreate(StudentBase):
    password: str

class TimetableBase(BaseModel):
    student_id: str
    day: str
    start_time: str
    end_time: str
    subject: str

class Timetable(TimetableBase):
    id: int
    class Config:
        orm_mode = True

class TodoBase(BaseModel):
    student_id: str
    title: str
    description: str
    due_date: datetime

class Todo(TodoBase):
    id: int
    completed: bool
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    student_id: Optional[str] = None

class Login(BaseModel):
    username: str
    password: str

class JWTToken(BaseModel):
    token: str
    expires_in: int