from fastapi.testclient import TestClient
from app.main import app
from app.utils.auth import authenticate_user
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate
from app.services import todo_service
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
import pytest

SQLALCHEMY_DATABASE_URL = f"sqlite:///./database/test_todo.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[settings.get_db] = override_get_db

client = TestClient(app)

def test_create_todo():
    user_data = {"username": "testuser", "password": "testpassword"}
    user = authenticate_user(user_data["username"], user_data["password"])
    if not user:
        user = todo_service.create_user(user_data)
    token = todo_service.create_token(user)
    headers = {"Authorization": f"Bearer {token}"}
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    response = client.post("/todos/", headers=headers, json=todo_data)
    assert response.status_code == 201
    assert response.json()["title"] == todo_data["title"]
    assert response.json()["description"] == todo_data["description"]

def test_read_todos():
    user_data = {"username": "testuser", "password": "testpassword"}
    user = authenticate_user(user_data["username"], user_data["password"])
    if not user:
        user = todo_service.create_user(user_data)
    token = todo_service.create_token(user)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/todos/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_todo():
    user_data = {"username": "testuser", "password": "testpassword"}
    user = authenticate_user(user_data["username"], user_data["password"])
    if not user:
        user = todo_service.create_user(user_data)
    token = todo_service.create_token(user)
    headers = {"Authorization": f"Bearer {token}"}
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    response = client.post("/todos/", headers=headers, json=todo_data)
    todo_id = response.json()["id"]
    response = client.get(f"/todos/{todo_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == todo_id
    assert response.json()["title"] == todo_data["title"]
    assert response.json()["description"] == todo_data["description"]

def test_update_todo():
    user_data = {"username": "testuser", "password": "testpassword"}
    user = authenticate_user(user_data["username"], user_data["password"])
    if not user:
        user = todo_service.create_user(user_data)
    token = todo_service.create_token(user)
    headers = {"Authorization": f"Bearer {token}"}
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    response = client.post("/todos/", headers=headers, json=todo_data)
    todo_id = response.json()["id"]
    updated_todo_data = {"title": "Updated Test Todo", "description": "This is an updated test todo"}
    response = client.put(f"/todos/{todo_id}", headers=headers, json=updated_todo_data)
    assert response.status_code == 200
    assert response.json()["id"] == todo_id
    assert response.json()["title"] == updated_todo_data["title"]
    assert response.json()["description"] == updated_todo_data["description"]

def test_delete_todo():
    user_data = {"username": "testuser", "password": "testpassword"}
    user = authenticate_user(user_data["username"], user_data["password"])
    if not user:
        user = todo_service.create_user(user_data)
    token = todo_service.create_token(user)
    headers = {"Authorization": f"Bearer {token}"}
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    response = client.post("/todos/", headers=headers, json=todo_data)
    todo_id = response.json()["id"]
    response = client.delete(f"/todos/{todo_id}", headers=headers)
    assert response.status_code == 200
    response = client.get(f"/todos/{todo_id}", headers=headers)
    assert response.status_code == 404

@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_todo_service_create_todo(db):
    user_data = {"username": "testuser", "password": "testpassword"}
    user = authenticate_user(user_data["username"], user_data["password"])
    if not user:
        user = todo_service.create_user(user_data)
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    todo = todo_service.create_todo(db, user.id, TodoCreate(**todo_data))
    assert todo.title == todo_data["title"]
    assert todo.description == todo_data["description"]

def test_todo_service_get_todos(db):
    user_data = {"username": "testuser", "password": "testpassword"}
    user = authenticate_user(user_data["username"], user_data["password"])
    if not user:
        user = todo_service.create_user(user_data)
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    todo = todo_service.create_todo(db, user.id, TodoCreate(**todo_data))
    todos = todo_service.get_todos(db, user.id)
    assert len(todos) == 1
    assert todos[0].title == todo_data["title"]
    assert todos[0].description == todo_data["description"]

def test_todo_service_get_todo(db):
    user_data = {"username": "testuser", "password": "testpassword"}
    user = authenticate_user(user_data["username"], user_data["password"])
    if not user:
        user = todo_service.create_user(user_data)
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    todo = todo_service.create_todo(db, user.id, TodoCreate(**todo_data))
    retrieved_todo = todo_service.get_todo(db, user.id, todo.id)
    assert retrieved_todo.title == todo_data["title"]
    assert retrieved_todo.description == todo_data["description"]

def test_todo_service_update_todo(db):
    user_data = {"username": "testuser", "password": "testpassword"}
    user = authenticate_user(user_data["username"], user_data["password"])
    if not user:
        user = todo_service.create_user(user_data)
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    todo = todo_service.create_todo(db, user.id, TodoCreate(**todo_data))
    updated_todo_data = {"title": "Updated Test Todo", "description": "This is an updated test todo"}
    updated_todo = todo_service.update_todo(db, user.id, todo.id, TodoUpdate(**updated_todo_data))
    assert updated_todo.title == updated_todo_data["title"]
    assert updated_todo.description == updated_todo_data["description"]

def test_todo_service_delete_todo(db):
    user_data = {"username": "testuser", "password": "testpassword"}
    user = authenticate_user(user_data["username"], user_data["password"])
    if not user:
        user = todo_service.create_user(user_data)
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    todo = todo_service.create_todo(db, user.id, TodoCreate(**todo_data))
    todo_service.delete_todo(db, user.id, todo.id)
    retrieved_todo = todo_service.get_todo(db, user.id, todo.id)
    assert retrieved_todo is None