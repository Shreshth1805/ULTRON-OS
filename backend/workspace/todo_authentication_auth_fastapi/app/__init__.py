from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes.todo import todo_router
from app.routes.user import user_router
from app.utils.auth import get_current_active_user

app = FastAPI(
    title=settings.PROJECT_TITLE,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    contact={
        "name": settings.PROJECT_CONTACT_NAME,
        "email": settings.PROJECT_CONTACT_EMAIL,
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_router, prefix="/todos", tags=["todos"])
app.include_router(user_router, prefix="/users", tags=["users"])

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.get("/me")
async def read_users_me(current_user = get_current_active_user):
    return current_user