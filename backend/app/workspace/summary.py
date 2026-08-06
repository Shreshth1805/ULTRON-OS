from pathlib import Path


class WorkspaceSummary:

    def summarize(self, project_path):

        project = Path(project_path)

        py_files = list(

            project.rglob("*.py")

        )

        return {

            "python_files": len(py_files),

            "folders": len(

                [p for p in project.rglob("*") if p.is_dir()]

            ),

            "files": len(

                [p for p in project.rglob("*") if p.is_file()]

            )

        }


workspace_summary = WorkspaceSummary()