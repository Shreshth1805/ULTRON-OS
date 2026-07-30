from pathlib import Path


# Only allow ULTRON to work inside this directory.
WORKSPACE = Path("ultron_workspace").resolve()

WORKSPACE.mkdir(
    parents=True,
    exist_ok=True
)


def safe_path(filename: str) -> Path:
    """
    Prevent path traversal such as ../../secret.txt
    """

    requested = (WORKSPACE / filename).resolve()

    if not requested.is_relative_to(WORKSPACE):
        raise ValueError(
            "Access outside ULTRON workspace is not allowed."
        )

    return requested


def list_files():
    """
    List files inside ULTRON workspace.
    """

    files = []

    for path in WORKSPACE.rglob("*"):

        if path.is_file():

            files.append(
                str(
                    path.relative_to(WORKSPACE)
                )
            )

    return files


def read_file(filename: str):
    """
    Read a text file from ULTRON workspace.
    """

    path = safe_path(filename)

    if not path.exists():

        raise FileNotFoundError(
            f"File not found: {filename}"
        )

    if not path.is_file():

        raise ValueError(
            "Requested path is not a file."
        )

    return path.read_text(
        encoding="utf-8"
    )


def write_file(
    filename: str,
    content: str
):
    """
    Write a text file inside ULTRON workspace.
    """

    path = safe_path(filename)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        content,
        encoding="utf-8"
    )

    return {
        "success": True,
        "file": str(
            path.relative_to(WORKSPACE)
        )
    }   