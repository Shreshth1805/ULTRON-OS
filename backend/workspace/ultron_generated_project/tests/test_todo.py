from fastapi.testclient import TestClient
from app.main import app
from app.utils.database import SessionLocal
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate
import pytest

@pytest.fixture
def client():
    return TestClient(app)

def test_create_todo(client):
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    response = client.post("/todos/", json=todo_data)
    assert response.status_code == 201
    assert response.json()["title"] == todo_data["title"]
    assert response.json()["description"] == todo_data["description"]

def test_read_todos(client):
    response = client.get("/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_todo(client):
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    response = client.post("/todos/", json=todo_data)
    todo_id = response.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == todo_data["title"]
    assert response.json()["description"] == todo_data["description"]

def test_update_todo(client):
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    response = client.post("/todos/", json=todo_data)
    todo_id = response.json()["id"]
    updated_todo_data = {"title": "Updated Test Todo", "description": "This is an updated test todo"}
    response = client.put(f"/todos/{todo_id}", json=updated_todo_data)
    assert response.status_code == 200
    assert response.json()["title"] == updated_todo_data["title"]
    assert response.json()["description"] == updated_todo_data["description"]

def test_delete_todo(client):
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    response = client.post("/todos/", json=todo_data)
    todo_id = response.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404

def test_create_todo_with_invalid_data(client):
    todo_data = {"title": "", "description": "This is a test todo"}
    response = client.post("/todos/", json=todo_data)
    assert response.status_code == 422

def test_update_todo_with_invalid_data(client):
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    response = client.post("/todos/", json=todo_data)
    todo_id = response.json()["id"]
    updated_todo_data = {"title": "", "description": "This is an updated test todo"}
    response = client.put(f"/todos/{todo_id}", json=updated_todo_data)
    assert response.status_code == 422

def test_delete_non_existent_todo(client):
    response = client.delete("/todos/99999")
    assert response.status_code == 404

def test_get_non_existent_todo(client):
    response = client.get("/todos/99999")
    assert response.status_code == 404

def test_get_all_todos_with_no_todos(client):
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []