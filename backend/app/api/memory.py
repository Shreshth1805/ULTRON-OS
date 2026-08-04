from fastapi import APIRouter

from app.memory.memory import memory

router = APIRouter(
    prefix="/memory",
    tags=["Memory"]
)


@router.get("/")
def get_history():

    return memory.history()


@router.delete("/")
def clear_history():

    memory.clear()

    return {

        "message": "Memory cleared"

    }