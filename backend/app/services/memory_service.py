from sqlalchemy.orm import Session

from app.models.memory import Memory


def save_memory(
    db: Session,
    user_id: int,
    content: str,
    memory_type: str = "conversation"
):

    memory = Memory(
        user_id=user_id,
        content=content,
        memory_type=memory_type
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory


def get_user_memories(
    db: Session,
    user_id: int,
    limit: int = 10
):

    return (
        db.query(Memory)
        .filter(Memory.user_id == user_id)
        .order_by(Memory.created_at.desc())
        .limit(limit)
        .all()
    )