from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.utils.auth import get_password_hash, verify_password
from app.models.todo import Todo

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    todos = relationship("Todo", back_populates="owner")

    def set_password(self, password):
        self.hashed_password = get_password_hash(password)

    def check_password(self, password):
        return verify_password(password, self.hashed_password)
    
    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, is_active={self.is_active})"