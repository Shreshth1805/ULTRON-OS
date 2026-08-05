from pathlib import Path


class Workspace:

    def __init__(self):

        self.root = Path("workspace")

        self.root.mkdir(
            exist_ok=True
        )

    def create_project(
        self,
        project_name
    ):

        project = self.root / project_name

        project.mkdir(
            exist_ok=True
        )

        return project

    def write_file(
        self,
        project,
        filename,
        content
    ):

        file = project / filename

        file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file.write_text(
            content,
            encoding="utf-8"
        )
        print(f"Created {file}")
        return str(file)


workspace = Workspace()