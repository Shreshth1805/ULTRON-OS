from pathlib import Path

from app.core.llm import llm


class CodeFixer:

    def fix(
        self,
        file_path,
        code,
        error
    ):

        prompt = f"""
You are an expert Python software engineer.

Fix the following code.

Error:

{error}

Current Code:

{code}

Return ONLY corrected code.
"""

        response = llm.invoke(prompt)

        fixed = response.content.strip()

        Path(file_path).write_text(
            fixed,
            encoding="utf-8"
        )

        return fixed


fixer = CodeFixer()