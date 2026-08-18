from pathlib import Path

from app.core.llm import llm

from app.agents.fixer.prompts import FIX_PROMPT

from app.agents.fixer.patcher import patcher

from app.agents.fixer.parser import extract_python


class FixerAgent:

    def fix_project(
        self,
        project_path,
        testing_result,
        entry_file="app/main.py"
    ):
        error = None

        if isinstance(testing_result, dict):
            error = testing_result.get("stderr") or testing_result.get("error")

        if not error:
            return {
                "success": False,
                "error": "No error information available to fix."
            }

        filename = str(Path(project_path) / entry_file)

        return self.fix(
            filename=filename,
            error=error
        )

    def fix(

        self,

        filename,

        error

    ):

        code = patcher.read(

            filename

        )

        prompt = FIX_PROMPT.format(

            filename=filename,

            code=code,

            error=error

        )

        response = llm.invoke(

            prompt

        )

        fixed = extract_python(

            response.content

        )

        patcher.write(

            filename,

            fixed

        )

        return {

            "success": True,

            "filename": filename

        }


fixer_agent = FixerAgent()