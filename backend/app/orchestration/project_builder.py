import re
from pathlib import Path

from app.generators.project_generator import project_generator
from app.generators.file_generator import file_generator

from app.orchestration.workspace import workspace
from app.execution.loop import execution_loop

from app.tools.registry import get_agent


class ProjectBuilder:

    def make_name(self, prompt: str) -> str:
        """
        Generate a safe project folder name.
        """

        name = re.sub(
            r"[^a-zA-Z0-9]+",
            "_",
            prompt.lower()
        ).strip("_")

        return name[:40] or "ultron_project"

    def build(self, prompt: str):

        # =====================================================
        # Planner Agent
        # =====================================================

        planner = get_agent(
            "planner_agent"
        )

        plan = {}

        if planner:

            try:

                plan = planner.create_plan(
                    prompt
                )

            except Exception as e:

                plan = {
                    "error": str(e)
                }

        # =====================================================
        # Project Name
        # =====================================================

        project_name = plan.get(
            "project_name"
        ) or self.make_name(prompt)

        project_path = workspace.create_project(
            project_name
        )

        # =====================================================
        # File Structure
        # =====================================================

        files = plan.get(
            "files",
            []
        )

        if not files:

            try:

                files = project_generator.get_structure(
                    prompt
                )

            except Exception as e:

                return {

                    "success": False,

                    "response": "Failed generating project structure.",

                    "error": str(e)

                }

        if not files:

            return {

                "success": False,

                "response": "Project contains no files."

            }

        # =====================================================
        # Generate Files
        # =====================================================

        generated_files = []

        for filename in files:

            try:

                code = file_generator.generate(

                    filename=filename,

                    project_description=prompt

                )

                workspace.write_file(

                    project=project_path,

                    filename=filename,

                    content=code

                )

                generated_files.append(
                    filename
                )

            except Exception as e:

                return {

                    "success": False,

                    "response": f"Failed generating {filename}",

                    "error": str(e)

                }

        # =====================================================
        # Execute Project
        # =====================================================

        execution_result = execution_loop.execute(

            project_path=str(project_path),

            entry_file="app/main.py"

        )

        # =====================================================
        # Review Agent
        # =====================================================

        review_result = None

        reviewer = get_agent(
            "reviewer_agent"
        )

        if reviewer:

            try:

                review_result = reviewer.review_project(

                    str(project_path)

                )

            except Exception as e:

                review_result = {

                    "success": False,

                    "error": str(e)

                }

        # =====================================================
        # Tester Agent
        # =====================================================

        testing_result = None

        tester = get_agent(
            "tester_agent"
        )

        if tester:

            try:

                testing_result = tester.test_project(

                    str(project_path)

                )

            except Exception as e:

                testing_result = {

                    "success": False,

                    "error": str(e)

                }

        # =====================================================
        # Project Statistics
        # =====================================================

        python_files = list(

            Path(project_path).rglob("*.py")

        )

        total_lines = 0

        total_size = 0

        for file in python_files:

            try:

                text = file.read_text(
                    encoding="utf-8"
                )

                total_lines += len(
                    text.splitlines()
                )

                total_size += len(
                    text.encode("utf-8")
                )

            except Exception:
                pass

        # =====================================================
        # Response
        # =====================================================

        return {

            "success": True,

            "project": project_name,

            "path": str(project_path),

            "plan": plan,

            "files": generated_files,

            "file_count": len(generated_files),

            "python_files": len(python_files),

            "lines_of_code": total_lines,

            "project_size_bytes": total_size,

            "execution": execution_result,

            "review": review_result,

            "testing": testing_result

        }


project_builder = ProjectBuilder()