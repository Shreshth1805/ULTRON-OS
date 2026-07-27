from fastapi import FastAPI
from app.api.health import router as health_router
from app.core.config import settings
from app.core.logger import logger
from app.database.init_db import init_db
from app.api.auth import router as auth_router
from app.api.users import router as user_router
app = FastAPI(

    title=settings.PROJECT_NAME,

    version=settings.VERSION
)

app.include_router(auth_router)
app.include_router(user_router)
@app.on_event("startup")
def startup():

    logger.info("Starting ULTRON")

    init_db()


app.include_router(health_router)


@app.get("/")
def root():

    logger.info("ULTRON Started")

    return {

        "name": settings.PROJECT_NAME,

        "version": settings.VERSION,

        "status": "Running"
    }

