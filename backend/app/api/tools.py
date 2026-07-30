from fastapi import APIRouter

from pydantic import BaseModel

from app.tools.registry import (
    list_tools,
    get_tool
)


router = APIRouter(
    prefix="/tools",
    tags=["Tools"]
)


class FileWriteRequest(BaseModel):

    filename: str

    content: str


class FileReadRequest(BaseModel):

    filename: str


class DatasetRequest(BaseModel):

    filename: str


class PythonValidationRequest(BaseModel):

    code: str


@router.get("/")
def available_tools():

    return {
        "tools": list_tools()
    }


@router.post("/write-file")
def write_file_endpoint(
    request: FileWriteRequest
):

    tool = get_tool(
        "write_file"
    )

    return tool(
        request.filename,
        request.content
    )


@router.post("/read-file")
def read_file_endpoint(
    request: FileReadRequest
):

    tool = get_tool(
        "read_file"
    )

    content = tool(
        request.filename
    )

    return {
        "content": content
    }


@router.post("/analyse-dataset")
def analyse_dataset_endpoint(
    request: DatasetRequest
):

    tool = get_tool(
        "analyse_dataset"
    )

    return tool(
        request.filename
    )


@router.post("/validate-python")
def validate_python_endpoint(
    request: PythonValidationRequest
):

    tool = get_tool(
        "validate_python_code"
    )

    return tool(
        request.code
    )