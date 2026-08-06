```python
import pytest
from auth import (
    verify_password,
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_active_user,
    get_user,
    fake_decode_token,
    Token,
    TokenData,
    User,
    UserInDB,
    pwd_context,
    oauth2_scheme,
)
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta

@pytest.fixture
def fake_db():
    return {"users": {}}

@pytest.fixture
def user():
    return UserInDB(
        username="johndoe",
        password=get_password_hash("secret"),
        email="johndoe@example.com",
        full_name="John Doe",
        disabled=False,
    )

def test_verify_password():
    assert verify_password("secret", get_password_hash("secret")) is True
    assert verify_password("wrong", get_password_hash("secret")) is False

def test_get_password_hash():
    password = "secret"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True

def test_authenticate_user(fake_db, user):
    fake_db["users"][user.username] = user.dict()
    assert authenticate_user(fake_db, user.username, "secret") == user
    assert authenticate_user(fake_db, user.username, "wrong") is False
    assert authenticate_user(fake_db, "wrong", "secret") is False

def test_create_access_token():
    access_token = create_access_token({"sub": "johndoe"})
    payload = jwt.decode(access_token, "secretkey", algorithms=["HS256"])
    assert payload["sub"] == "johndoe"
    assert "exp" in payload

def test_get_current_user():
    access_token = create_access_token({"sub": "johndoe"})
    with pytest.raises(HTTPException):
        get_current_user(token="wrong")
    user = get_current_user(token=access_token)
    assert user.username == "johndoe"

def test_get_current_active_user():
    access_token = create_access_token({"sub": "johndoe"})
    user = get_current_user(token=access_token)
    with pytest.raises(HTTPException):
        get_current_active_user(current_user=UserInDB(**{"username": "johndoe", "password": get_password_hash("secret"), "email": "johndoe@example.com", "full_name": "John Doe", "disabled": True}))
    get_current_active_user(current_user=user)

def test_get_user(fake_db, user):
    fake_db["users"][user.username] = user.dict()
    assert get_user(fake_db, user.username) == user
    assert get_user(fake_db, "wrong") is None

def test_fake_decode_token():
    user = fake_decode_token("johndoe")
    assert user.username == "johndoe"
```