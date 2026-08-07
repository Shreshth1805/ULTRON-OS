from fastapi import APIRouter

from app.llm.manager import (
    llm_manager
)

router = APIRouter(
    prefix="/llm",
    tags=["LLM"]
)


@router.get("/models")
def models():

    return {

        "models":

        llm_manager.available_models()

    }


@router.get("/health")
def health():

    return llm_manager.health()