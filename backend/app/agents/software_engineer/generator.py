from app.core.llm import llm


class CodeGenerator:

    def generate_file(
        self,
        filename,
        project_description,
        project_plan
    ):

        prompt = f"""
Project:

{project_description}

Plan:

{project_plan}

Generate ONLY the code for

{filename}

No markdown.
"""

        response = llm.invoke(prompt)

        return response.content


generator = CodeGenerator()