from app.core.llm import llm


class ProjectPlanner:

    def create_plan(self, request: str):

        prompt = f"""
You are a Senior Software Architect.

Create a development plan for:

{request}

Return:

Project Name

Folder Structure

Files

Development Steps
"""

        response = llm.invoke(prompt)

        return response.content


planner = ProjectPlanner()