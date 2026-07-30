from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.memory import (
    MemoryCreate,
    MemoryResponse
)

from app.services.memory_service import (
    save_memory,
    get_user_memories
)

from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/memory",
    tags=["Memory"]
)


@router.post(
    "/",
    response_model=MemoryResponse
)
def create_memory(
    memory: MemoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return save_memory(
        db=db,
        user_id=current_user.id,
        content=memory.content,
        memory_type=memory.memory_type
    )


@router.get(
    "/",
    response_model=list[MemoryResponse]
)
def read_memories(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_user_memories(
        db=db,
        user_id=current_user.id
    )