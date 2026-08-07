from app.core.llm import llm


class CodeGenerator:

    def generate_file(
        self,
        filename,
        project_description,
        project_plan
    ):

        prompt = f"""
You are ULTRON's senior software engineer.

You are building a real software project.

PROJECT REQUEST:
{project_description}

PROJECT ARCHITECTURE:
{project_plan}

You must generate the complete contents of:

{filename}

Rules:

1. Generate ONLY the file contents.
2. Do NOT use markdown code fences.
3. Do NOT explain the code.
4. The file must work with the other project files.
5. Follow the architecture in the project plan.
6. Use production-quality code.
7. Include proper imports.
8. Do not create fake placeholder implementations unless absolutely necessary.
9. Do not omit important functionality.
10. Maintain compatibility with the rest of the project.

Generate:

{filename}
"""

        response = llm.invoke(
            prompt
        )

        return getattr(
            response,
            "content",
            str(response)
        )


generator = CodeGenerator()