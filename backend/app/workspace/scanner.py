from pathlib import Path


class WorkspaceScanner:

    def scan(self, project_path: str):

        project = Path(project_path)

        files = []

        for file in project.rglob("*"):

            if file.is_file():

                files.append({

                    "path": str(file.relative_to(project)),

                    "size": file.stat().st_size

                })

        return files


workspace_scanner = WorkspaceScanner()