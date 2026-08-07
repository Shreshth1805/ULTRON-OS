from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.database.init_db import init_db

# ==========================================================
# API ROUTERS
# ==========================================================

from app.api.ai import router as ai_router
from app.api.tools import router as tools_router
from app.api.automl import router as automl_router
from app.api.memory import router as memory_router
from app.api.knowledge import router as knowledge_router
import app.monitoring.workflow_monitor
from app.projects.router import (
    router as projects_router
)

from app.projects.file_router import (
    router as project_file_router
)
from app.api.llm import (
    router as llm_router
)
from app.api.semantic_memory import (

    router as semantic_memory_router

)

# ==========================================================
# APPLICATION LIFESPAN
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("===================================")
    print("Starting ULTRON...")
    print("Initializing Database...")
    print("===================================")

    init_db()

    yield

    print("===================================")
    print("Shutting down ULTRON...")
    print("===================================")


# ==========================================================
# FASTAPI APP
# ==========================================================

app = FastAPI(

    title=settings.PROJECT_NAME,

    version=settings.VERSION,

    lifespan=lifespan

)

# ==========================================================
# ROUTERS
# ==========================================================

app.include_router(ai_router)

app.include_router(tools_router)

app.include_router(automl_router)

app.include_router(memory_router)

app.include_router(projects_router)

app.include_router(project_file_router)

app.include_router(knowledge_router)

app.include_router(llm_router)

app.include_router(semantic_memory_router)

# ==========================================================
# ROOT
# ==========================================================

@app.get("/")
def root():

    return {

        "project": settings.PROJECT_NAME,

        "version": settings.VERSION,

        "status": "online",

        "llm": "Groq",

        "model": settings.GROQ_MODEL,

        "modules": [

            "AI",

            "Software Engineer",

            "AutoML",

            "Knowledge Base",

            "Memory",

            "Projects",

            "Tools"

        ]

    }


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/health")
def health():

    return {

        "status": "healthy",

        "database": "connected",

        "llm": "Groq",

        "memory": "enabled",

        "knowledge": "enabled"

    }


# ==========================================================
# INFO
# ==========================================================

@app.get("/info")
def info():

    return {

        "name": settings.PROJECT_NAME,

        "version": settings.VERSION,

        "framework": "FastAPI",

        "llm": settings.GROQ_MODEL,

        "database": settings.DATABASE_URL,

        "features": [

            "Chat",

            "Project Generation",

            "Software Engineer Agent",

            "AutoML",

            "Memory",

            "Knowledge RAG",

            "Project Builder",

            "Reviewer",

            "Tester"

        ]

    }