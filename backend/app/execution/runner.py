import sys
import subprocess
from pathlib import Path


TIMEOUT_SECONDS = 30


class CodeRunner:

    def run(self, project_path: str, entry_file: str = "app/main.py"):

        file_path = Path(project_path) / entry_file

        if not file_path.exists():
            return {
                "success": False,
                "stdout": "",
                "stderr": f"{entry_file} not found."
            }

        # Run as a module (`-m app.main`) rather than as a script
        # (`python app/main.py`), with cwd set to the project root.
        # This lets the project's own internal absolute imports (e.g.
        # `uvicorn.run("app.main:app")`, `from app.main import app`)
        # resolve correctly, the same way they would once the project
        # is actually deployed - running as a bare script instead puts
        # only the entry file's own directory on sys.path, so any
        # "app.something" import inside it fails with
        # "No module named 'app'" even though the code is otherwise
        # correct.
        module_name = entry_file[:-3] if entry_file.endswith(".py") else entry_file
        module_name = module_name.replace("/", ".").replace("\\", ".")

        try:

            result = subprocess.run(
                [sys.executable, "-m", module_name],
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

            # A generated web app whose entry point starts a real
            # server (uvicorn.run(...)) never exits on its own - that's
            # not necessarily a bug in the generated code, just not
            # something a one-shot subprocess check can distinguish
            # from "hung". Report it distinctly so callers don't waste
            # fix attempts trying to "fix" a server that's simply
            # still running.
            return {
                "success": False,
                "stdout": (e.stdout or ""),
                "stderr": (
                    f"TIMEOUT: process did not exit within "
                    f"{TIMEOUT_SECONDS}s. If this entry point starts a "
                    f"server (e.g. uvicorn.run(...)), that may be "
                    f"expected rather than a bug."
                )
            }


runner = CodeRunner()
