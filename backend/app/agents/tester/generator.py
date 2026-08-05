from app.core.llm import llm
from app.agents.tester.prompts import TEST_PROMPT


class TestGenerator:

    def generate(
        self,
        filename,
        code
    ):

        prompt = f"""
{TEST_PROMPT}

Filename:

{filename}

Code:

{code}
"""

        response = llm.invoke(prompt)

        return response.content.strip()


test_generator = TestGenerator()