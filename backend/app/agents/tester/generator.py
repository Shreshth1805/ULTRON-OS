from pathlib import Path

from app.core.llm import llm

from app.agents.tester.prompts import TEST_PROMPT


class TestGenerator:

    def generate_tests(self, project_path: str):

        project = Path(project_path)

        generated = []

        for file in project.rglob("*.py"):

            if file.name.startswith("test_"):
                continue

            try:

                code = file.read_text(
                    encoding="utf-8"
                )

                prompt = TEST_PROMPT.format(
                    code=code
                )

                response = llm.invoke(
                    prompt
                )

                test_file = file.parent / f"test_{file.name}"

                test_file.write_text(
                    response.content,
                    encoding="utf-8"
                )

                generated.append(
                    str(test_file)
                )

            except Exception:
                pass

        return generated


test_generator = TestGenerator()