from app.database.session import engine

from app.models.base import Base

from app.models.user import User
from app.models.conversation import Conversation

from app.projects.models import Project


def init_db():

    Base.metadata.create_all(
        bind=engine
    )