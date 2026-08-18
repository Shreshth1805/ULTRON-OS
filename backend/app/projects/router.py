from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.projects.schemas import (
    ProjectCreate,
    ProjectResponse
)

from app.projects.service import (
    create_project,
    get_project,
    get_projects,
    delete_project
)

from app.orchestration.project_builder import project_builder


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


class ProjectBuildRequest(BaseModel):

    prompt: str


# =========================================================
# DATABASE DEPENDENCY
# =========================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =========================================================
# BUILD (full autonomous pipeline)
# =========================================================

@router.post(
    "/build"
)
def build_project(
    request: ProjectBuildRequest
):

    if not request.prompt or not request.prompt.strip():

        raise HTTPException(
            status_code=400,
            detail="prompt must not be empty."
        )

    return project_builder.build(
        request.prompt
    )


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",
    response_model=ProjectResponse
)
def create_project_endpoint(
    request: ProjectCreate,
    db: Session = Depends(get_db)
):

    try:

        return create_project(
            db=db,
            name=request.name,
            description=request.description
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# =========================================================
# LIST
# =========================================================

@router.get(
    "/",
    response_model=list[ProjectResponse]
)
def list_projects(
    db: Session = Depends(get_db)
):

    return get_projects(db)


# =========================================================
# GET
# =========================================================

@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def project_details(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = get_project(
        db,
        project_id
    )

    if project is None:

        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )

    return project


# =========================================================
# DELETE
# =========================================================

@router.delete(
    "/{project_id}"
)
def remove_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = delete_project(
        db,
        project_id
    )

    if project is None:

        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )

    return {
        "success": True,
        "message": "Project deleted."
    }