from fastapi.testclient import TestClient
from app.main import app
from app.utils.auth import authenticate_user
from app.models.user import User
from app.schemas.user import UserCreate
from app.services import get_user_service
from app.utils import get_db
from sqlalchemy.orm import Session
import pytest

client = TestClient(app)

@pytest.fixture
def db():
    db = next(get_db())
    yield db
    db.close()

def test_root(db: Session):
    response = client.get("/")
    assert response.status_code == 200

def test_create_user(db: Session):
    user_data = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    user = get_user_service.get_user_by_username(db, username=user_data["username"])
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]

def test_get_user(db: Session):
    user_data = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    client.post("/users/", json=user_data)
    response = client.get("/users/testuser")
    assert response.status_code == 200
    user = response.json()
    assert user["username"] == user_data["username"]
    assert user["email"] == user_data["email"]

def test_login_user(db: Session):
    user_data = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    client.post("/users/", json=user_data)
    response = client.post("/token", data={"username": user_data["username"], "password": user_data["password"]})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None

def test_create_todo(db: Session):
    user_data = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    client.post("/users/", json=user_data)
    response = client.post("/token", data={"username": user_data["username"], "password": user_data["password"]})
    token = response.json()["access_token"]
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    response = client.post("/todos/", json=todo_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    todo = response.json()
    assert todo["title"] == todo_data["title"]
    assert todo["description"] == todo_data["description"]

def test_get_todos(db: Session):
    user_data = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    client.post("/users/", json=user_data)
    response = client.post("/token", data={"username": user_data["username"], "password": user_data["password"]})
    token = response.json()["access_token"]
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    client.post("/todos/", json=todo_data, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/todos/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["title"] == todo_data["title"]
    assert todos[0]["description"] == todo_data["description"]