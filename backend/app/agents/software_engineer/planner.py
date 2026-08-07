from app.core.llm import llm


class ProjectPlanner:

    def create_plan(
        self,
        request: str
    ):

        prompt = f"""
You are ULTRON's Senior Software Architect.

Design a COMPLETE software project for this request:

{request}

Your response MUST contain these sections:

Project Name:
<name>

Project Description:
<description>

Folder Structure:
<complete folder structure>

Files:
<one file per line>

Development Steps:
<numbered steps>

Dependencies:
<dependencies>

IMPORTANT:

1. Include EVERY file required for the project.
2. Do not limit the project to main.py.
3. Include backend files.
4. Include frontend files if required.
5. Include configuration files.
6. Include tests.
7. Include README.md.
8. Include requirements.txt or the appropriate dependency file.
9. Include database files/models if required.
10. Include Docker files if useful.
11. Make the architecture production-ready.
12. Do not generate source code here.
"""

        response = llm.invoke(
            prompt
        )

        return getattr(
            response,
            "content",
            str(response)
        )


planner = ProjectPlanner()