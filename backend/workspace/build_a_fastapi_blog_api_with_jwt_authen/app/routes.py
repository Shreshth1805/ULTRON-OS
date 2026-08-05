from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from app import crud, models, schemas
from app.database import SessionLocal

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(db, username: str):
    return crud.get_user(db, username)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not crud.verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret_key", algorithm="HS256")
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "secret_key", algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db = SessionLocal()
    user = get_user(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not crud.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(SessionLocal(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@router.post("/posts/")
async def create_post(post: schemas.PostCreate, db: SessionLocal = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return crud.create_post(db, post, current_user)

@router.get("/posts/")
async def read_posts(db: SessionLocal = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return crud.get_posts(db)

@router.get("/posts/{post_id}")
async def read_post(post_id: int, db: SessionLocal = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return crud.get_post(db, post_id)

@router.put("/posts/{post_id}")
async def update_post(post_id: int, post: schemas.PostCreate, db: SessionLocal = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return crud.update_post(db, post_id, post, current_user)

@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, db: SessionLocal = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return crud.delete_post(db, post_id)