```python
import pytest
from fastapi.testclient import TestClient
from main import app, verify_password, get_password_hash, authenticate_user, create_access_token, fake_db
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

@pytest.fixture
def client():
    return TestClient(app)

class UserIn(BaseModel):
    username: str
    email: str
    full_name: str
    password: str

class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool

class Token(BaseModel):
    access_token: str
    token_type: str

def test_verify_password():
    password = "password123"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password)

def test_get_password_hash():
    password = "password123"
    hashed_password = get_password_hash(password)
    assert hashed_password

def test_authenticate_user():
    fake_db["test_user"] = UserIn(username="test_user", email="test@example.com", full_name="Test User", password=get_password_hash("password123"))
    user = authenticate_user(fake_db, "test_user", "password123")
    assert user

def test_create_access_token():
    access_token = create_access_token(data={"sub": "test_user"})
    assert access_token

def test_create_user(client):
    user = UserIn(username="test_user", email="test@example.com", full_name="Test User", password="password123")
    response = client.post("/users/", json=user.dict())
    assert response.status_code == 200
    assert response.json()["username"] == user.username

def test_login(client):
    user = UserIn(username="test_user", email="test@example.com", full_name="Test User", password="password123")
    client.post("/users/", json=user.dict())
    response = client.post("/token", data={"grant_type": "password", "username": user.username, "password": user.password})
    assert response.status_code == 200
    assert response.json()["access_token"]

def test_get_current_user(client):
    user = UserIn(username="test_user", email="test@example.com", full_name="Test User", password="password123")
    client.post("/users/", json=user.dict())
    response = client.post("/token", data={"grant_type": "password", "username": user.username, "password": user.password})
    access_token = response.json()["access_token"]
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == user.username

def test_create_student(client):
    user = UserIn(username="test_user", email="test@example.com", full_name="Test User", password="password123")
    client.post("/users/", json=user.dict())
    response = client.post("/token", data={"grant_type": "password", "username": user.username, "password": user.password})
    access_token = response.json()["access_token"]
    student = {"id": 1, "name": "John Doe", "email": "johndoe@example.com"}
    response = client.post("/students/", json=student, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["name"] == student["name"]

def test_get_students(client):
    user = UserIn(username="test_user", email="test@example.com", full_name="Test User", password="password123")
    client.post("/users/", json=user.dict())
    response = client.post("/token", data={"grant_type": "password", "username": user.username, "password": user.password})
    access_token = response.json()["access_token"]
    response = client.get("/students/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_timetable(client):
    user = UserIn(username="test_user", email="test@example.com", full_name="Test User", password="password123")
    client.post("/users/", json=user.dict())
    response = client.post("/token", data={"grant_type": "password", "username": user.username, "password": user.password})
    access_token = response.json()["access_token"]
    timetable = {"id": 1, "student_id": 1, "day": "Monday", "time": "10:00", "subject": "Math"}
    response = client.post("/timetables/", json=timetable, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["subject"] == timetable["subject"]

def test_get_timetables(client):
    user = UserIn(username="test_user", email="test@example.com", full_name="Test User", password="password123")
    client.post("/users/", json=user.dict())
    response = client.post("/token", data={"grant_type": "password", "username": user.username, "password": user.password})
    access_token = response.json()["access_token"]
    response = client.get("/timetables/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_todo(client):
    user = UserIn(username="test_user", email="test@example.com", full_name="Test User", password="password123")
    client.post("/users/", json=user.dict())
    response = client.post("/token", data={"grant_type": "password", "username": user.username, "password": user.password})
    access_token = response.json()["access_token"]
    todo = {"id": 1, "student_id": 1, "title": "Do Homework", "description": "Finish math homework", "due_date": "2024-03-16"}
    response = client.post("/todos/", json=todo, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["title"] == todo["title"]

def test_get_todos(client):
    user = UserIn(username="test_user", email="test@example.com", full_name="Test User", password="password123")
    client.post("/users/", json=user.dict())
    response = client.post("/token", data={"grant_type": "password", "username": user.username, "password": user.password})
    access_token = response.json()["access_token"]
    response = client.get("/todos/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0
```