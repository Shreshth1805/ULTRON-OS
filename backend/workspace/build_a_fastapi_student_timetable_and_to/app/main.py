from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import List, Optional

app = FastAPI()

# Configuration
SECRET_KEY = "secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Context
pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT Token
class Token(BaseModel):
    access_token: str
    token_type: str

# Token Data
class TokenData(BaseModel):
    username: Optional[str] = None

# User Model
class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool

# User In Model
class UserIn(BaseModel):
    username: str
    email: str
    full_name: str
    password: str

# Student Model
class Student(BaseModel):
    id: int
    name: str
    email: str

# Timetable Model
class Timetable(BaseModel):
    id: int
    student_id: int
    day: str
    time: str
    subject: str

# Todo Model
class Todo(BaseModel):
    id: int
    student_id: int
    title: str
    description: str
    due_date: str

# Verify Password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Get Password Hash
def get_password_hash(password):
    return pwd_context.hash(password)

# Authenticate User
def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Create Access Token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Get Current User
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = fake_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Fake Database
fake_db = {}

# Create User
@app.post("/users/")
async def create_user(user: UserIn):
    hashed_password = get_password_hash(user.password)
    user_h = UserIn(username=user.username, email=user.email, full_name=user.full_name, password=hashed_password)
    fake_db[user.username] = user_h
    return user

# Login
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Get Current User
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Create Student
@app.post("/students/")
async def create_student(student: Student, current_user: User = Depends(get_current_user)):
    return student

# Get Students
@app.get("/students/")
async def read_students(current_user: User = Depends(get_current_user)):
    return [{"id": 1, "name": "John Doe", "email": "johndoe@example.com"}]

# Create Timetable
@app.post("/timetables/")
async def create_timetable(timetable: Timetable, current_user: User = Depends(get_current_user)):
    return timetable

# Get Timetables
@app.get("/timetables/")
async def read_timetables(current_user: User = Depends(get_current_user)):
    return [{"id": 1, "student_id": 1, "day": "Monday", "time": "10:00", "subject": "Math"}]

# Create Todo
@app.post("/todos/")
async def create_todo(todo: Todo, current_user: User = Depends(get_current_user)):
    return todo

# Get Todos
@app.get("/todos/")
async def read_todos(current_user: User = Depends(get_current_user)):
    return [{"id": 1, "student_id": 1, "title": "Do Homework", "description": "Finish math homework", "due_date": "2024-03-16"}]