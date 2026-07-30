from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.models.conversation import Conversation


def save_message(
    session_id: str,
    role: str,
    message: str
):

    db: Session = SessionLocal()

    try:

        conversation = Conversation(
            session_id=session_id,
            role=role,
            message=message
        )

        db.add(conversation)

        db.commit()

        db.refresh(conversation)

        return conversation

    finally:

        db.close()


def get_history(
    session_id: str,
    limit: int = 20
):

    db: Session = SessionLocal()

    try:

        conversations = (
            db.query(Conversation)
            .filter(
                Conversation.session_id == session_id
            )
            .order_by(
                Conversation.created_at.asc()
            )
            .limit(limit)
            .all()
        )

        return [
            {
                "role": item.role,
                "message": item.message,
                "created_at": item.created_at
            }
            for item in conversations
        ]

    finally:

        db.close()


def clear_history(
    session_id: str
):

    db: Session = SessionLocal()

    try:

        db.query(
            Conversation
        ).filter(
            Conversation.session_id == session_id
        ).delete()

        db.commit()

    finally:

        db.close()