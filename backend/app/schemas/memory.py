from datetime import datetime

from pydantic import BaseModel


class MemoryCreate(BaseModel):

    content: str

    memory_type: str = "conversation"


class MemoryResponse(BaseModel):

    id: int

    user_id: int

    content: str

    memory_type: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }