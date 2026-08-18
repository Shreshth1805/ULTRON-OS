import sys
import subprocess


TIMEOUT_SECONDS = 60


class TestRunner:

    def run(self, project_path: str):

        try:

            # Use this interpreter's own `-m pytest` rather than a bare
            # "pytest" off PATH, so tests run against the same
            # environment (and its installed packages) as the rest of
            # the app instead of whatever interpreter happens to be
            # first on PATH.
            result = subprocess.run(
                [sys.executable, "-m", "pytest"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS
            )

            return {

                "success": result.returncode == 0,

                "stdout": result.stdout,

                "stderr": result.stderr

            }

        except subprocess.TimeoutExpired as e:

            return {

                "success": False,

                "stdout": (e.stdout or ""),

                "stderr": f"TIMEOUT: tests did not complete within {TIMEOUT_SECONDS}s."

            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)

            }


test_runner = TestRunner()