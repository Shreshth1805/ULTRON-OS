from pathlib import Path


WORKSPACE_ROOT = Path("workspace")


def get_project_path(
    project_name: str
):

    return (
        WORKSPACE_ROOT /
        project_name
    )


# =========================================================
# WRITE FILE
# =========================================================

def write_project_file(
    project_name: str,
    filename: str,
    content: str
):

    project_path = get_project_path(
        project_name
    )

    project_path.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = (
        project_path /
        filename
    )

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path.write_text(
        content,
        encoding="utf-8"
    )

    return {
        "success": True,
        "filename": filename,
        "path": str(file_path)
    }


# =========================================================
# READ FILE
# =========================================================

def read_project_file(
    project_name: str,
    filename: str
):

    file_path = (
        get_project_path(project_name) /
        filename
    )

    if not file_path.exists():

        return {
            "success": False,
            "error": "File does not exist."
        }

    content = file_path.read_text(
        encoding="utf-8"
    )

    return {
        "success": True,
        "filename": filename,
        "content": content
    }


# =========================================================
# LIST FILES
# =========================================================

def list_project_files(
    project_name: str
):

    project_path = get_project_path(
        project_name
    )

    if not project_path.exists():

        return []

    files = []

    for file in project_path.rglob("*"):

        if file.is_file():

            files.append(
                str(
                    file.relative_to(
                        project_path
                    )
                )
            )

    return files


# =========================================================
# DELETE FILE
# =========================================================

def delete_project_file(
    project_name: str,
    filename: str
):

    file_path = (
        get_project_path(project_name) /
        filename
    )

    if not file_path.exists():

        return {
            "success": False,
            "error": "File does not exist."
        }

    file_path.unlink()

    return {
        "success": True,
        "message": "File deleted."
    }