from app.core.llm import llm
from app.generators.prompts import SYSTEM_PROMPT
from app.utils.text import strip_code_fence


class FileGenerator:

    def generate(
        self,
        filename,
        project_description,
        other_files=None
    ):

        files_note = ""

        if other_files:

            file_list = "\n".join(
                f"- {f}" for f in other_files if f != filename
            )

            files_note = f"""
This project's full file list is:

{file_list}

Only define each responsibility (routes, models, app setup, etc.) once
across the whole project. If another file already defines something
(e.g. a router or an endpoint), import and use it from there instead of
redefining it here.
"""

        prompt = f"""
{SYSTEM_PROMPT}

Project:

{project_description}
{files_note}
Generate ONLY the contents of

{filename}
"""

        response = llm.invoke(prompt)

        return strip_code_fence(response.content)


file_generator = FileGenerator()