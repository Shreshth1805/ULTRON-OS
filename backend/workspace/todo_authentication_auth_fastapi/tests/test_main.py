import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.auth import authenticate_user
from app.models.user import User
from app.schemas.user import UserCreate
from app.services import get_user_service
from app.utils import get_db
from sqlalchemy.orm import Session

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_create_user():
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"]

def test_get_user():
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    user_id = response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]

def test_login_user():
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    response = client.post("/login", data={"username": user_data["username"], "password": user_data["password"]})
    assert response.status_code == 200
    assert response.json()["access_token"] is not None

def test_get_user_with_token():
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    response = client.post("/login", data={"username": user_data["username"], "password": user_data["password"]})
    token = response.json()["access_token"]
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]

def test_create_todo():
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    response = client.post("/login", data={"username": user_data["username"], "password": user_data["password"]})
    token = response.json()["access_token"]
    todo_data = {"title": "testtodo", "description": "testdescription"}
    response = client.post("/todos/", json=todo_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json()["title"] == todo_data["title"]

def test_get_todo():
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    response = client.post("/login", data={"username": user_data["username"], "password": user_data["password"]})
    token = response.json()["access_token"]
    todo_data = {"title": "testtodo", "description": "testdescription"}
    response = client.post("/todos/", json=todo_data, headers={"Authorization": f"Bearer {token}"})
    todo_id = response.json()["id"]
    response = client.get(f"/todos/{todo_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == todo_data["title"]

def test_update_todo():
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    response = client.post("/login", data={"username": user_data["username"], "password": user_data["password"]})
    token = response.json()["access_token"]
    todo_data = {"title": "testtodo", "description": "testdescription"}
    response = client.post("/todos/", json=todo_data, headers={"Authorization": f"Bearer {token}"})
    todo_id = response.json()["id"]
    updated_todo_data = {"title": "updatedtesttodo", "description": "updatedtestdescription"}
    response = client.put(f"/todos/{todo_id}", json=updated_todo_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == updated_todo_data["title"]

def test_delete_todo():
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    response = client.post("/login", data={"username": user_data["username"], "password": user_data["password"]})
    token = response.json()["access_token"]
    todo_data = {"title": "testtodo", "description": "testdescription"}
    response = client.post("/todos/", json=todo_data, headers={"Authorization": f"Bearer {token}"})
    todo_id = response.json()["id"]
    response = client.delete(f"/todos/{todo_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_unauthorized_access():
    response = client.get("/users/me")
    assert response.status_code == 401

def test_invalid_token():
    response = client.get("/users/me", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401

def test_invalid_user():
    response = client.post("/login", data={"username": "invaliduser", "password": "invalidpassword"})
    assert response.status_code == 401

@pytest.fixture
def db():
    db = next(get_db())
    yield db
    db.close()

def test_create_user_with_db(db: Session):
    user_data = UserCreate(username="testuser", password="testpassword")
    user = get_user_service().create_user(db, user_data)
    assert user.username == user_data.username

def test_get_user_with_db(db: Session):
    user_data = UserCreate(username="testuser", password="testpassword")
    user = get_user_service().create_user(db, user_data)
    retrieved_user = get_user_service().get_user(db, user.id)
    assert retrieved_user.username == user_data.username

def test_authenticate_user_with_db(db: Session):
    user_data = UserCreate(username="testuser", password="testpassword")
    user = get_user_service().create_user(db, user_data)
    authenticated_user = authenticate_user(db, user_data.username, user_data.password)
    assert authenticated_user.username == user_data.username