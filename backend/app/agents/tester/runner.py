import subprocess


class TestRunner:

    def run(self, project_path: str):

        try:

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

        except Exception as e:

            return {

                "success": False,

                "error": str(e)

            }


test_runner = TestRunner()