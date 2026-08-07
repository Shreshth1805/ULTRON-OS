from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import todo
from app.utils import config

app = FastAPI(
    title="TodoAPI",
    description="A FastAPI-based RESTful API for managing todo items",
    version="1.0.0"
)

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo.router, prefix="/todo", tags=["todo"])

@app.on_event("startup")
async def startup_event():
    await config.initialize_database()

@app.on_event("shutdown")
async def shutdown_event():
    await config.close_database()