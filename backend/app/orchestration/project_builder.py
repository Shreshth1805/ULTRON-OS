import re

from app.orchestration.workspace import workspace

from app.orchestration.templates import FASTAPI_TEMPLATE


class ProjectBuilder:

    def build(
        self,
        prompt: str
    ):

        project_name = self.make_name(
            prompt
        )

        project = workspace.create_project(
            project_name
        )

        created = []

        for filename, content in FASTAPI_TEMPLATE.items():

            workspace.write_file(
                project,
                filename,
                content
            )

            created.append(filename)

        return {

            "success": True,

            "project": project_name,

            "files": created

        }

    def make_name(
        self,
        prompt
    ):

        name = re.sub(
            r"[^a-zA-Z0-9]+",
            "_",
            prompt.lower()
        )

        return name[:30]


project_builder = ProjectBuilder()