from app.workspace.scanner import workspace_scanner
from app.workspace.tree import workspace_tree
from app.workspace.search import workspace_search
from app.workspace.editor import workspace_editor
from app.workspace.summary import workspace_summary


class WorkspaceManager:

    def scan(self, project):

        return workspace_scanner.scan(project)

    def tree(self, project):

        return workspace_tree.build(project)

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

        return workspace_summary.summarize(project)


workspace_manager = WorkspaceManager()