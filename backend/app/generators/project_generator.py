from app.core.llm import llm
from app.generators.prompts import SYSTEM_PROMPT


class ProjectGenerator:

    def get_structure(
        self,
        description
    ):

        prompt = f"""
{SYSTEM_PROMPT}

Project:

{description}

Return ONLY a file list.

Example:

app/main.py

app/routes.py

requirements.txt

README.md

Dockerfile
"""

        response = llm.invoke(prompt)

        files = []

        for line in response.content.splitlines():

            line = line.strip()

            if line:

                files.append(line)

        return files


project_generator = ProjectGenerator()