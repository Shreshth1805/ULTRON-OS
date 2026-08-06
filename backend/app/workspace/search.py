from pathlib import Path


class WorkspaceSearch:

    def search(

        self,

        project_path,

        keyword

    ):

        project = Path(project_path)

        matches = []

        for file in project.rglob("*.py"):

            try:

                lines = file.read_text(
                    encoding="utf-8"
                ).splitlines()

                for i, line in enumerate(lines, 1):

                    if keyword.lower() in line.lower():

                        matches.append({

                            "file": str(file.relative_to(project)),

                            "line": i,

                            "text": line

                        })

            except Exception:
                pass

        return matches


workspace_search = WorkspaceSearch()