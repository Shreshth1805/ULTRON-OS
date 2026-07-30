from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.chat.chat_agent import chat_agent


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):

    session_id: str = "default"

    message: str


class ClearMemoryRequest(BaseModel):

    session_id: str = "default"


@router.post("/")
def chat(
    request: ChatRequest
):

    return chat_agent.chat(
        session_id=request.session_id,
        message=request.message
    )


@router.delete("/memory/{session_id}")
def clear_memory(
    session_id: str
):

    from app.memory.manager import memory_manager

    memory_manager.clear_session(
        session_id
    )

    return {
        "message": "Conversation memory cleared",
        "session_id": session_id
    }