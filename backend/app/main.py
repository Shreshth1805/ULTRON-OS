from fastapi import FastAPI

from app.core.config import settings

from app.database.init_db import init_db

from app.api.ai import router as ai_router
from app.api.tools import router as tools_router
from app.api.automl import router as automl_router

from app.projects.router import (
    router as projects_router
)

from app.projects.file_router import (
    router as project_file_router
)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)


@app.on_event("startup")
def startup():

    init_db()


app.include_router(
    ai_router
)

app.include_router(
    tools_router
)

app.include_router(
    automl_router
)

app.include_router(
    projects_router
)

app.include_router(
    project_file_router
)


@app.get("/")
def root():

    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online"
    }