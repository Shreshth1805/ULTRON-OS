from pathlib import Path


class ProjectReviewer:

    def load_project(self, project_path: str):

        code = []

        project = Path(project_path)

        for file in project.rglob("*.py"):

            try:

                text = file.read_text(
                    encoding="utf-8"
                )

                code.append(
                    f"\n# File: {file.relative_to(project)}\n\n{text}"
                )

            except Exception:
                pass

        return "\n".join(code)


reviewer = ProjectReviewer()