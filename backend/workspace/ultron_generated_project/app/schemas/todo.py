from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TodoResponse(BaseModel):
    success: bool
    data: Optional[Todo] = None
    error: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "id": 1,
                    "title": "Example Todo",
                    "description": "This is an example todo item",
                    "created_at": "2022-01-01T00:00:00",
                    "updated_at": "2022-01-01T00:00:00"
                },
                "error": None
            }
        }