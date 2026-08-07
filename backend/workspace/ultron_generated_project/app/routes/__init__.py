from fastapi import APIRouter
from .todo import todo_router

router = APIRouter()

router.include_router(todo_router, prefix="/todo", tags=["todo"])