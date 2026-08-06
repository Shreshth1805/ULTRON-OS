from fastapi import APIRouter

from pydantic import BaseModel

from app.knowledge import (

    index_document,

    ask

)

router = APIRouter(

    prefix="/knowledge",

    tags=["Knowledge"]

)


class IndexRequest(BaseModel):

    filename: str


class QuestionRequest(BaseModel):

    question: str


@router.post("/index")

def index(

    request: IndexRequest

):

    return index_document(

        request.filename

    )


@router.post("/ask")

def ask_question(

    request: QuestionRequest

):

    return ask(

        request.question

    )