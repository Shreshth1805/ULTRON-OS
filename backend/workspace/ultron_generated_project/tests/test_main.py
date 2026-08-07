from fastapi.testclient import TestClient
from app.main import app
from app.utils.database import SessionLocal
from app.models.todo import Todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.utils.config import settings

SQLALCHEMY_DATABASE_URL = f"sqlite:///./test_{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client():
    from app.main import get_db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200

def test_create_todo(client):
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test Description"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Todo"
    assert response.json()["description"] == "Test Description"

def test_read_todos(client):
    response = client.get("/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_todo(client):
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test Description"})
    todo_id = response.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["id"] == todo_id
    assert response.json()["title"] == "Test Todo"
    assert response.json()["description"] == "Test Description"

def test_update_todo(client):
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test Description"})
    todo_id = response.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"title": "Updated Test Todo", "description": "Updated Test Description"})
    assert response.status_code == 200
    assert response.json()["id"] == todo_id
    assert response.json()["title"] == "Updated Test Todo"
    assert response.json()["description"] == "Updated Test Description"

def test_delete_todo(client):
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test Description"})
    todo_id = response.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404