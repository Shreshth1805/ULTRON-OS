from fastapi import APIRouter

from app.memory_v2 import (

    memory_manager,

    memory_retriever

)

router = APIRouter(

    prefix="/semantic-memory",

    tags=["Semantic Memory"]

)


@router.post("/remember")

def remember(

    session_id: str,

    role: str,

    message: str

):

    memory_manager.remember(

        session_id,

        role,

        message

    )

    return {

        "success": True

    }


@router.get("/search")

def search(

    query: str

):

    return memory_retriever.search(

        query

    )