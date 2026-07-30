from app.database.session import engine

from app.models.base import Base

# Import models so SQLAlchemy knows about them
from app.models.conversation import Conversation
from app.models.user import User
from app.models.base import Base

def init_db():

    Base.metadata.create_all(
        bind=engine
    )