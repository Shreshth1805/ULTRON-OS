from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class StudentBase(BaseModel):
    student_id: str
    name: str
    email: str

class StudentCreate(StudentBase):
    password: str

class Student(StudentBase):
    id: int
    password: str
    timetable: List[dict] = []
    todo_list: List[dict] = []
    class Config:
        orm_mode = True

class StudentLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class TimetableBase(BaseModel):
    day: str
    period: str
    subject: str
    room: str

class TimetableCreate(TimetableBase):
    pass

class Timetable(TimetableBase):
    id: int
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
    completed: bool = False
    class Config:
        orm_mode = True