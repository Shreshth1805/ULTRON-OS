from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from app.utils.auth import get_current_user
from app.models.todo import Todo
from app.schemas.todo import TodoSchema, TodoCreateSchema
from app.services import todo_service

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[TodoSchema])
async def read_todos(current_user: str = Depends(get_current_user)):
    todos = await todo_service.get_all_todos(current_user)
    return todos

@router.get("/{todo_id}", response_model=TodoSchema)
async def read_todo(todo_id: int, current_user: str = Depends(get_current_user)):
    todo = await todo_service.get_todo(todo_id, current_user)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.post("/", response_model=TodoSchema)
async def create_todo(todo: TodoCreateSchema, current_user: str = Depends(get_current_user)):
    new_todo = await todo_service.create_todo(todo, current_user)
    return new_todo

@router.put("/{todo_id}", response_model=TodoSchema)
async def update_todo(todo_id: int, todo: TodoCreateSchema, current_user: str = Depends(get_current_user)):
    updated_todo = await todo_service.update_todo(todo_id, todo, current_user)
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, current_user: str = Depends(get_current_user)):
    deleted = await todo_service.delete_todo(todo_id, current_user)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Todo deleted successfully"})