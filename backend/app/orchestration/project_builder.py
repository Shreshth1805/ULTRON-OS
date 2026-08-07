import re
from pathlib import Path

from app.generators.project_generator import project_generator
from app.generators.file_generator import file_generator

from app.orchestration.workspace import workspace
from app.execution.loop import execution_loop

from app.tools.registry import get_agent
from app.bus import Event, dispatcher

class ProjectBuilder:

    def make_name(self, prompt: str) -> str:
        """
        Generate a safe project name.
        """

        name = re.sub(
            r"[^a-zA-Z0-9]+",
            "_",
            prompt.lower()
        ).strip("_")

        return name[:40] or "ultron_project"

    def build(self, prompt: str):

        # =====================================================
        # Planner
        # =====================================================

        planner = get_agent("planner_agent")

        plan = {}

        if planner:

            try:

                plan = planner.create_plan(prompt)

            except Exception as e:

                plan = {
                    "success": False,
                    "error": str(e)
                }

        # =====================================================
        # Project Name
        # =====================================================

        project_name = self.make_name(prompt)

        if isinstance(plan, dict):

            project_name = plan.get(
                "project_name",
                project_name
            )

        project_path = workspace.create_project(
            project_name
        )

        # =====================================================
        # Project Structure
        # =====================================================

        files = []

        if isinstance(plan, dict):

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
                "response": "No files generated."
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

                generated_files.append(filename)

            except Exception as e:

                return {
                    "success": False,
                    "response": f"Failed generating {filename}",
                    "error": str(e)
                }

        # =====================================================
        # Execute Project
        # =====================================================

        try:

            execution_result = execution_loop.execute(
                project_path=str(project_path),
                entry_file="app/main.py"
            )

        except Exception as e:

            execution_result = {
                "success": False,
                "error": str(e)
            }
        event = Event(

            type="PROJECT_CREATED",

            source="project_builder",

            payload={

                "project_name": project_name,

                "project_path": str(project_path),

                "code": project_code

            }

        )

        event_results = dispatcher.emit(
            event
        )            

        # =====================================================
        # Review
        # =====================================================

        review_result = None

        reviewer = get_agent("reviewer_agent")

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
        # Security Review
        # =====================================================

        security_result = None

        security = get_agent("security_agent")

        if security:

            try:

                code = ""

                for file in Path(project_path).rglob("*.py"):

                    code += file.read_text(
                        encoding="utf-8"
                    )

                    code += "\n\n"

                security_result = security.review(code)

            except Exception as e:

                security_result = {
                    "success": False,
                    "error": str(e)
                }

        # =====================================================
        # Testing
        # =====================================================

        testing_result = None

        tester = get_agent("tester_agent")

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
        # Auto Fix
        # =====================================================

        fixer_result = None

        fixer = get_agent("fixer_agent")

        if (
            fixer
            and isinstance(testing_result, dict)
            and not testing_result.get("success", True)
        ):

            try:

                fixer_result = fixer.fix_project(
                    str(project_path),
                    testing_result
                )

            except Exception as e:

                fixer_result = {
                    "success": False,
                    "error": str(e)
                }

        # =====================================================
        # Reflection
        # =====================================================

        reflection_result = None

        reflection = get_agent("reflection_agent")

        if reflection:

            try:

                reflection_result = reflection.reflect(
                    project=project_name,
                    execution=execution_result,
                    review=review_result,
                    security=security_result,
                    performance=performance_result,
                    testing=testing_result,
                    review=review_result
                )

            except Exception as e:

                reflection_result = {
                    "success": False,
                    "error": str(e)
                }
            learner = get_agent(
                "learner_agent"
            )

            learning_result = None

            if learner:

                try:

                    learning_result = learner.learn(

                        project=project_name,

                        review=review_result,

                        testing=testing_result,

                        reflection=reflection_result

                    )

                except Exception as e:

                    learning_result = {

                        "success": False,

                        "error": str(e)

                    }                
        # =====================================================
        # Security Review
        # =====================================================

        security_result = None

        security = get_agent(
            "security_agent"
        )

        if security:

            try:

                security_result = security.review(
                    project_code
                )

            except Exception as e:

                security_result = {

                    "success": False,

                    "error": str(e)

                } 
        # =====================================================
        # Performance Review
        # =====================================================
        performance_result = None
        performance = get_agent(
            "performance_agent"
        )
        if performance:

            try:

                performance_result = performance.analyze(
                    project_code
                )

            except Exception as e:

                performance_result = {

                    "success": False,

                    "error": str(e)
                }                               
        # =====================================================
        # Load Project Source Code Once
        # =====================================================

        python_files = list(
            Path(project_path).rglob("*.py")
        )

        project_code = ""

        for file in python_files:

            try:

                project_code += file.read_text(
                    encoding="utf-8"
                )

                project_code += "\n\n"

            except Exception:
                pass  

        version_result = None

        version = get_agent(
            "version_agent"
        )

        if version:

            try:

                version_result = version.save(

                    project=project_name,

                    files=generated_files,

                    message="Initial Generated Project"

                )

            except Exception as e:

                version_result = {

                    "success": False,

                    "error": str(e)

                }                 
        # =====================================================
        # GitHub
        # =====================================================

        github_result = None

        github = get_agent("github_agent")

        if github:

            try:

                github_result = github.publish(
                    project_name=project_name,
                    project_path=str(project_path)
                )

            except Exception as e:

                github_result = {
                    "success": False,
                    "error": str(e)
                }

        # =====================================================
        # Statistics
        # =====================================================

        python_files = list(
            Path(project_path).rglob("*.py")
        )

        total_lines = 0
        total_size = 0
        total_files = 0

        for file in Path(project_path).rglob("*"):

            if file.is_file():

                total_files += 1

                try:

                    total_size += file.stat().st_size

                except Exception:
                    pass

        for file in python_files:

            try:

                text = file.read_text(
                    encoding="utf-8"
                )

                total_lines += len(
                    text.splitlines()
                )

            except Exception:
                pass

        # =====================================================
        # Final Response
        # =====================================================

        return {

            "success": True,

            "project": project_name,

            "path": str(project_path),

            "plan": plan,

            "files": generated_files,

            "file_count": len(generated_files),

            "total_files": total_files,

            "python_files": len(python_files),

            "lines_of_code": total_lines,

            "project_size_bytes": total_size,

            "execution": execution_result,

            "review": review_result,

            "security": security_result,

            "testing": testing_result,

            "fixes": fixer_result,

            "reflection": reflection_result,

            "github": github_result,

            "learning": learning_result,

            "version": version_result,

            "events": event_results,

        }


project_builder = ProjectBuilder()