import subprocess
from pathlib import Path


class CodeRunner:

    def run(self, project_path: str, entry_file: str = "app/main.py"):

        file_path = Path(project_path) / entry_file

        if not file_path.exists():
            return {
                "success": False,
                "stdout": "",
                "stderr": f"{entry_file} not found."
            }

        result = subprocess.run(
            ["python", str(file_path)],
            capture_output=True,
            text=True
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }


runner = CodeRunner()