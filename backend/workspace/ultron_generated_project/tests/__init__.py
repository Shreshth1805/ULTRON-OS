from fastapi.testclient import TestClient
from app.main import app
from app.utils.database import engine
from app.models import todo
from app.schemas import todo as todo_schema
import pytest

client = TestClient(app)

@pytest.fixture
def db():
    todo.Base.metadata.create_all(bind=engine)
    yield
    todo.Base.metadata.drop_all(bind=engine)

def test_main():
    response = client.get("/")
    assert response.status_code == 200

def test_create_todo(db):
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test Description"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Todo"
    assert response.json()["description"] == "Test Description"

def test_get_all_todos(db):
    client.post("/todos/", json={"title": "Test Todo 1", "description": "Test Description 1"})
    client.post("/todos/", json={"title": "Test Todo 2", "description": "Test Description 2"})
    response = client.get("/todos/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_todo(db):
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test Description"})
    todo_id = response.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"
    assert response.json()["description"] == "Test Description"

def test_update_todo(db):
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test Description"})
    todo_id = response.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"title": "Updated Test Todo", "description": "Updated Test Description"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Todo"
    assert response.json()["description"] == "Updated Test Description"

def test_delete_todo(db):
    response = client.post("/todos/", json={"title": "Test Todo", "description": "Test Description"})
    todo_id = response.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404