from pathlib import Path

from app.execution.runner import runner
from app.execution.debugger import debugger
from app.execution.fixer import fixer


class ExecutionLoop:

    def execute(
        self,
        project_path,
        entry_file="app/main.py",
        max_attempts=3
    ):

        file_path = Path(project_path) / entry_file

        for attempt in range(max_attempts):

            result = runner.run(
                project_path,
                entry_file
            )

            if result["success"]:
                return {
                    "success": True,
                    "attempts": attempt + 1,
                    "stdout": result["stdout"]
                }

            analysis = debugger.analyze(
                result["stderr"]
            )

            if not analysis["has_error"]:
                break

            current_code = file_path.read_text(
                encoding="utf-8"
            )

            fixer.fix(
                file_path=file_path,
                code=current_code,
                error=analysis["error"]
            )

        return {
            "success": False,
            "stderr": result["stderr"]
        }


execution_loop = ExecutionLoop()