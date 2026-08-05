import subprocess
from pathlib import Path


class TestRunner:

    def run(
        self,
        project_path
    ):

        result = subprocess.run(

            ["pytest"],

            cwd=project_path,

            capture_output=True,

            text=True

        )

        return {

            "success": result.returncode == 0,

            "stdout": result.stdout,

            "stderr": result.stderr

        }


test_runner = TestRunner()