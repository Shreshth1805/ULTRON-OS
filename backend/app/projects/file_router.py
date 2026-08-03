from fastapi import (
    APIRouter,
    HTTPException
)

from pydantic import BaseModel

from app.workspace.file_manager import (
    write_project_file,
    read_project_file,
    list_project_files,
    delete_project_file
)


router = APIRouter(
    prefix="/projects",
    tags=["Project Files"]
)


class FileRequest(BaseModel):

    filename: str


class WriteFileRequest(BaseModel):

    filename: str

    content: str


# =========================================================
# LIST PROJECT FILES
# =========================================================

@router.get("/{project_name}/files")
def list_files(
    project_name: str
):

    return {
        "project": project_name,
        "files": list_project_files(
            project_name
        )
    }


# =========================================================
# WRITE FILE
# =========================================================

@router.post("/{project_name}/files")
def write_file(
    project_name: str,
    request: WriteFileRequest
):

    return write_project_file(
        project_name=project_name,
        filename=request.filename,
        content=request.content
    )


# =========================================================
# READ FILE
# =========================================================

@router.post("/{project_name}/files/read")
def read_file(
    project_name: str,
    request: FileRequest
):

    result = read_project_file(
        project_name=project_name,
        filename=request.filename
    )

    if not result["success"]:

        raise HTTPException(
            status_code=404,
            detail=result["error"]
        )

    return result


# =========================================================
# DELETE FILE
# =========================================================

@router.delete("/{project_name}/files")
def delete_file(
    project_name: str,
    request: FileRequest
):

    result = delete_project_file(
        project_name=project_name,
        filename=request.filename
    )

    if not result["success"]:

        raise HTTPException(
            status_code=404,
            detail=result["error"]
        )

    return result