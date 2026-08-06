from pathlib import Path


class WorkspaceTree:

    def build(self, project_path: str):

        project = Path(project_path)

        tree = []

        for path in sorted(project.rglob("*")):

            depth = len(path.relative_to(project).parts)

            tree.append({

                "depth": depth,

                "path": str(path.relative_to(project))

            })

        return tree


workspace_tree = WorkspaceTree()