from pydantic import BaseModel


class AutoMLRequest(BaseModel):

    filename: str

    target_column: str


class AutoMLResponse(BaseModel):

    status: str

    message: str = ""

    results: dict = {}