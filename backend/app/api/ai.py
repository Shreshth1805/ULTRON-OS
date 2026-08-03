from fastapi import APIRouter
from pydantic import BaseModel

from app.orchestration.brain import process_request

from app.agents.software_engineer.engineer import (
    software_engineer_agent
)

from app.memory.service import (
    get_history,
    clear_history
)


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


# =========================================================
# REQUEST MODELS
# =========================================================

class CodeRequest(BaseModel):

    code: str

    filename: str = "main.py"


class ChatRequest(BaseModel):

    message: str

    session_id: str = "default"


# =========================================================
# CHAT
# =========================================================

@router.post("/chat")
def chat(
    request: ChatRequest
):

    return process_request(
        message=request.message,
        session_id=request.session_id
    )


# =========================================================
# CODE GENERATION
# =========================================================

@router.post("/code")
def generate_code(
    request: CodeRequest
):

    return software_engineer_agent.generate_code(
        code=request.code,
        filename=request.filename
    )


# =========================================================
# CODE TESTING
# =========================================================

@router.post("/code/test")
def test_code(
    request: CodeRequest
):

    return software_engineer_agent.test_code(
        request.code
    )


# =========================================================
# GET CONVERSATION MEMORY
# =========================================================

@router.get("/memory/{session_id}")
def conversation_history(
    session_id: str
):

    return {
        "session_id": session_id,
        "history": get_history(
            session_id=session_id
        )
    }


# =========================================================
# CLEAR CONVERSATION MEMORY
# =========================================================

@router.delete("/memory/{session_id}")
def delete_conversation(
    session_id: str
):

    clear_history(
        session_id=session_id
    )

    return {
        "success": True,
        "message": "Conversation memory cleared."
    }

class ProjectRequest(BaseModel):

    project_name: str

    description: str

@router.post("/project/build")
def build_project(

    request: ProjectRequest

):

    return software_engineer_agent.build_project(

        request.project_name,

        request.description

    )    