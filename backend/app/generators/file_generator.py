from app.core.llm import llm
from app.generators.prompts import SYSTEM_PROMPT


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

        return response.content.strip()


file_generator = FileGenerator()