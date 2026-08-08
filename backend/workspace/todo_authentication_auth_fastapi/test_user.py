from fastapi.testclient import TestClient
from app.main import app
from app.utils.auth import get_password_hash
from app.models.user import User
from app.database import SessionLocal
from sqlalchemy.orm import sessionmaker
from app.schemas.user import UserCreate

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_user():
    db = next(get_db())
    user_in = UserCreate(email="test@example.com", password="test")
    user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    assert user.email == user_in.email

def test_get_user():
    db = next(get_db())
    user_in = UserCreate(email="test@example.com", password="test")
    user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    client = TestClient(app)
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["email"] == user_in.email

def test_get_users():
    db = next(get_db())
    user_in1 = UserCreate(email="test1@example.com", password="test")
    user1 = User(email=user_in1.email, hashed_password=get_password_hash(user_in1.password))
    db.add(user1)
    db.commit()
    db.refresh(user1)
    user_in2 = UserCreate(email="test2@example.com", password="test")
    user2 = User(email=user_in2.email, hashed_password=get_password_hash(user_in2.password))
    db.add(user2)
    db.commit()
    db.refresh(user2)
    client = TestClient(app)
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_update_user():
    db = next(get_db())
    user_in = UserCreate(email="test@example.com", password="test")
    user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    client = TestClient(app)
    new_email = "new@example.com"
    response = client.put(f"/users/{user.id}", json={"email": new_email})
    assert response.status_code == 200
    assert response.json()["email"] == new_email

def test_delete_user():
    db = next(get_db())
    user_in = UserCreate(email="test@example.com", password="test")
    user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    client = TestClient(app)
    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted"

def test_login_user():
    db = next(get_db())
    user_in = UserCreate(email="test@example.com", password="test")
    user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    client = TestClient(app)
    response = client.post("/login", json={"email": user_in.email, "password": user_in.password})
    assert response.status_code == 200
    assert response.json()["access_token"] is not None

def test_login_user_invalid_credentials():
    db = next(get_db())
    user_in = UserCreate(email="test@example.com", password="test")
    user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    client = TestClient(app)
    response = client.post("/login", json={"email": user_in.email, "password": "wrong"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_user_non_existent():
    db = next(get_db())
    client = TestClient(app)
    response = client.post("/login", json={"email": "non_existent@example.com", "password": "test"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"