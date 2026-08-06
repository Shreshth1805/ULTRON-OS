from app.core.llm import llm

from app.agents.fixer.prompts import FIX_PROMPT

from app.agents.fixer.patcher import patcher

from app.agents.fixer.parser import extract_python


class FixerAgent:

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