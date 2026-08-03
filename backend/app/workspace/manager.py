from pathlib import Path


# =========================================================
# WORKSPACE ROOT
# =========================================================

WORKSPACE_ROOT = Path("workspace")

WORKSPACE_ROOT.mkdir(
    exist_ok=True
)


# =========================================================
# CREATE PROJECT
# =========================================================

def create_project_directory(
    project_name: str
):

    safe_name = project_name.strip()

    project_path = (
        WORKSPACE_ROOT /
        safe_name
    )

    project_path.mkdir(
        parents=True,
        exist_ok=True
    )

    return project_path


# =========================================================
# DELETE PROJECT DIRECTORY
# =========================================================

def delete_project_directory(
    project_name: str
):

    project_path = (
        WORKSPACE_ROOT /
        project_name
    )

    if not project_path.exists():

        return False

    import shutil

    shutil.rmtree(
        project_path
    )

    return True


# =========================================================
# PROJECT EXISTS
# =========================================================

def project_exists(
    project_name: str
):

    project_path = (
        WORKSPACE_ROOT /
        project_name
    )

    return project_path.exists()


# =========================================================
# LIST PROJECTS
# =========================================================

def list_project_directories():

    if not WORKSPACE_ROOT.exists():

        return []

    return [
        item.name
        for item in WORKSPACE_ROOT.iterdir()
        if item.is_dir()
    ]