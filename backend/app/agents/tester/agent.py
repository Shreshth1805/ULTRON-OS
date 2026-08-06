from app.agents.tester.generator import test_generator
from app.agents.tester.runner import test_runner


class TesterAgent:

    def test_project(self, project_path: str):

        tests = test_generator.generate_tests(
            project_path
        )

        results = test_runner.run(
            project_path
        )

        return {

            "success": True,

            "generated_tests": tests,

            "results": results

        }


tester_agent = TesterAgent()