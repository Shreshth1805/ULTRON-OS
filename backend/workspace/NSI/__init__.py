from .main import app
from .config import settings
from .database import engine, SessionLocal
from .models import Base
from .utils import auth, errors
from .services import node_service, workflow_service
from .routes import nodes, workflows

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()