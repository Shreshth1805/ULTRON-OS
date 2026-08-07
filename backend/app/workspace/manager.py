from pathlib import Path
from app.workspace.scanner import workspace_scanner
from app.workspace.tree import workspace_tree
from app.workspace.search import workspace_search
from app.workspace.editor import workspace_editor
from app.workspace.summary import workspace_summary
# =========================================================
# WORKSPACE ROOT
# =========================================================
# All ULTRON projects will be stored here.
# Change this location later if you want a different workspace.
WORKSPACE_ROOT = Path("workspace")
# Make sure the workspace directory exists.
WORKSPACE_ROOT.mkdir(
    parents=True,
    exist_ok=True
)
# =========================================================
# PROJECT DIRECTORY MANAGEMENT
# =========================================================
def create_project_directory(name: str) -> Path:
    """
    Create and return the directory for a project.
    """
    project_path = WORKSPACE_ROOT / name
    project_path.mkdir(
        parents=True,
        exist_ok=True
    )
    return project_path
def delete_project_directory(name: str) -> bool:
    """
    Delete a project's workspace directory.
    Returns:
        True  -> directory deleted
        False -> directory did not exist
    """
    import shutil
    project_path = WORKSPACE_ROOT / name
    if not project_path.exists():
        return False
    if not project_path.is_dir():
        raise ValueError(
            f"Project path is not a directory: {project_path}"
        )
    shutil.rmtree(
        project_path
    )
    return True
# =========================================================
# WORKSPACE MANAGER
# =========================================================
class WorkspaceManager:
    def scan(self, project):
        return workspace_scanner.scan(
            project
        )
    def tree(self, project):
        return workspace_tree.build(
            project
        )
    def search(
        self,
        project,
        keyword
    ):
        return workspace_search.search(
            project,
            keyword
        )
    def replace(
        self,
        project,
        filename,
        content
    ):
        return workspace_editor.replace(
            project,
            filename,
            content
        )
    def summary(self, project):
        return workspace_summary.summarize(
            project
        )
workspace_manager = WorkspaceManager()