from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
def health():

    return {

        "status": "healthy",

        "timestamp": datetime.utcnow(),

        "service": "ULTRON Backend"
    }