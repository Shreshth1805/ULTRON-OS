from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlalchemy.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class StudentTimetable(Base):
    __tablename__ = "student_timetable"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    subject = Column(String, index=True)
    time = Column(DateTime, index=True)

class TodoList(Base):
    __tablename__ = "todo_list"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    task = Column(String, index=True)
    deadline = Column(DateTime, index=True)

Base.metadata.create_all(bind=engine)