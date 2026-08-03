import subprocess
from pathlib import Path


class ProjectExecutor:

    def run_python(
        self,
        file_path
    ):

        try:

            result = subprocess.run(

                ["python", file_path],

                capture_output=True,

                text=True

            )

            return {

                "stdout": result.stdout,

                "stderr": result.stderr,

                "returncode": result.returncode

            }

        except Exception as e:

            return {

                "error": str(e)

            }


executor = ProjectExecutor()