from app.database.database import engine

from app.models.base import Base

from app.models.user import User


def init_db():

    Base.metadata.create_all(bind=engine)