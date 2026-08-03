from datetime import datetime

from pydantic import BaseModel


class ProjectCreate(BaseModel):

    name: str

    description: str = ""


class ProjectResponse(BaseModel):

    id: int

    name: str

    description: str | None

    project_path: str

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True