from sqlalchemy.orm import Session

from app.projects.models import Project

from app.workspace.manager import (
    create_project_directory,
    delete_project_directory
)


# =========================================================
# CREATE PROJECT
# =========================================================

def create_project(
    db: Session,
    name: str,
    description: str = ""
):

    existing = (
        db.query(Project)
        .filter(
            Project.name == name
        )
        .first()
    )

    if existing:

        raise ValueError(
            "Project already exists."
        )

    project_path = (
        create_project_directory(
            name
        )
    )

    project = Project(

        name=name,

        description=description,

        project_path=str(
            project_path
        )
    )

    db.add(project)

    db.commit()

    db.refresh(project)

    return project


# =========================================================
# GET PROJECT
# =========================================================

def get_project(
    db: Session,
    project_id: int
):

    return (
        db.query(Project)
        .filter(
            Project.id == project_id
        )
        .first()
    )


# =========================================================
# LIST PROJECTS
# =========================================================

def get_projects(
    db: Session
):

    return (
        db.query(Project)
        .order_by(
            Project.created_at.desc()
        )
        .all()
    )


# =========================================================
# DELETE PROJECT
# =========================================================

def delete_project(
    db: Session,
    project_id: int
):

    project = get_project(
        db,
        project_id
    )

    if project is None:

        return None

    delete_project_directory(
        project.name
    )

    db.delete(project)

    db.commit()

    return project