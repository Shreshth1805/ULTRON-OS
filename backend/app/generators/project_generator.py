from app.core.llm import llm
from app.generators.prompts import SYSTEM_PROMPT
from app.utils.text import strip_code_fence, looks_like_file_path


class ProjectGenerator:

    def get_structure(
        self,
        description
    ):

        prompt = f"""
{SYSTEM_PROMPT}

Project:

{description}

Return ONLY a file list: one relative file path per line, nothing else.

No comments, no shell commands, no explanations, no numbering or
bullets - just the paths themselves.

Example:

app/main.py

app/routes.py

requirements.txt

README.md

Dockerfile
"""

        response = llm.invoke(prompt)

        files = []

        for line in strip_code_fence(response.content).splitlines():

            line = line.strip()

            if line and looks_like_file_path(line):

                files.append(line)

        return files


project_generator = ProjectGenerator()