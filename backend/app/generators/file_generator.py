from app.core.llm import llm
from app.generators.prompts import SYSTEM_PROMPT
from app.utils.text import strip_code_fence


class FileGenerator:

    def generate(
        self,
        filename,
        project_description
    ):

        prompt = f"""
{SYSTEM_PROMPT}

Project:

{project_description}

Generate ONLY the contents of

{filename}
"""

        response = llm.invoke(prompt)

        return strip_code_fence(response.content)


file_generator = FileGenerator()