from pathlib import Path

from app.agents.tester.generator import (
    test_generator
)

from app.agents.tester.runner import (
    test_runner
)


class TesterAgent:

    def test_project(
        self,
        project_path
    ):

        project = Path(project_path)

        generated = []

        for file in project.rglob("*.py"):

            if file.name.startswith("test_"):
                continue

            code = file.read_text(
                encoding="utf-8"
            )

            tests = test_generator.generate(
                file.name,
                code
            )

            test_file = file.parent / (
                "test_" + file.name
            )

            test_file.write_text(
                tests,
                encoding="utf-8"
            )

            generated.append(
                str(test_file)
            )

        result = test_runner.run(
            project_path
        )

        return {

            "success": True,

            "generated_tests": generated,

            "pytest": result

        }


tester_agent = TesterAgent()