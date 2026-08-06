from pathlib import Path


class WorkspaceEditor:

    def replace(

        self,

        project_path,

        filename,

        content

    ):

        file = Path(project_path) / filename

        file.write_text(

            content,

            encoding="utf-8"

        )

        return True


workspace_editor = WorkspaceEditor()